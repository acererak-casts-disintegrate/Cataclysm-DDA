#include <algorithm>
#include <climits>
#include <map>
#include <set>
#include <string>
#include <vector>

#include "activity_type.h"
#include "avatar.h"
#include "calendar.h"
#include "cata_catch.h"
#include "coordinates.h"
#include "inventory.h"
#include "item_factory.h"
#include "item_group.h"
#include "item_location.h"
#include "item.h"
#include "itype.h"
#include "iuse_actor.h"
#include "map_selector.h"
#include "map.h"
#include "map_helpers.h"
#include "material.h"
#include "player_activity.h"
#include "player_helpers.h"
#include "point.h"
#include "recipe.h"
#include "recipe_dictionary.h"
#include "requirements.h"
#include "type_id.h"
#include "units.h"
#include "veh_type.h"
#include "vehicle.h"
#include "vpart_position.h"

// Tests for the 3D Printing mod (data/mods/3D_Printing); they do nothing when it is not loaded.

static const activity_id ACT_REPAIR_ITEM( "ACT_REPAIR_ITEM" );

static const itype_id itype_3d_printer_advanced( "3d_printer_advanced" );
static const itype_id itype_3d_printer_basic( "3d_printer_basic" );
static const itype_id itype_carbon_fiber_filament( "carbon_fiber_filament" );
static const itype_id itype_knife_combat( "knife_combat" );

static const material_id material_carbonfiber( "carbonfiber" );

static const requirement_id requirement_data_3d_printing_metal( "3d_printing_metal" );

static const vpart_id vpart_3d_printer_advancedrig( "3d_printer_advancedrig" );
static const vpart_id vpart_3d_printer_basicrig( "3d_printer_basicrig" );
static const vpart_id vpart_frame( "frame" );
static const vpart_id vpart_small_storage_battery( "small_storage_battery" );

static const vproto_id vehicle_prototype_none( "none" );

static bool printing_mod_loaded()
{
    return itype_3d_printer_basic.is_valid();
}

static bool is_printer( const itype_id &type )
{
    return type == itype_3d_printer_basic || type == itype_3d_printer_advanced;
}

// Recipes that print with a printer, or build one into something
static bool uses_printer( const recipe &r )
{
    for( const std::vector<tool_comp> &alternatives : r.simple_requirements().get_tools() ) {
        for( const tool_comp &tool : alternatives ) {
            if( is_printer( tool.type ) ) {
                return true;
            }
        }
    }
    for( const std::vector<item_comp> &alternatives : r.simple_requirements().get_components() ) {
        for( const item_comp &comp : alternatives ) {
            if( is_printer( comp.type ) ) {
                return true;
            }
        }
    }
    return false;
}

// The lightest mass of components the recipe can be made from
static units::mass lightest_inputs( const recipe &r )
{
    units::mass total = 0_gram;
    for( const std::vector<item_comp> &alternatives : r.simple_requirements().get_components() ) {
        units::mass lightest = units::mass::max();
        for( const item_comp &comp : alternatives ) {
            if( comp.type.is_valid() ) {
                lightest = std::min( lightest, comp.type->weight * comp.count );
            }
        }
        if( lightest != units::mass::max() ) {
            total += lightest;
        }
    }
    return total;
}

static units::mass output_mass( const recipe &r )
{
    units::mass total = 0_gram;
    for( const item &it : r.create_results() ) {
        total += it.weight();
    }
    for( const item &it : r.create_byproducts() ) {
        total += it.weight();
    }
    return total;
}

// A printer only shapes what it is fed, so nothing it prints may outweigh the lightest set of
// components it can be printed from.  The same goes for the rigs a printer is built into.
TEST_CASE( "printed_items_conserve_mass", "[recipe][3d_printing]" )
{
    if( !printing_mod_loaded() ) {
        return;
    }
    int checked = 0;
    for( const auto &[id, r] : recipe_dict ) {
        if( r.obsolete || r.is_blacklisted() || !uses_printer( r ) ) {
            continue;
        }
        ++checked;
        const units::mass in = lightest_inputs( r );
        const units::mass out = output_mass( r );
        CAPTURE( id.str(), units::to_gram( in ), units::to_gram( out ) );
        CHECK( in >= out );
    }
    CHECK( checked > 50 );
}

TEST_CASE( "only_the_advanced_printer_sinters_metal", "[recipe][3d_printing]" )
{
    if( !printing_mod_loaded() ) {
        return;
    }
    const requirement_data &metal = requirement_data_3d_printing_metal.obj();
    REQUIRE( metal.get_tools().size() == 1 );
    for( const tool_comp &tool : metal.get_tools().front() ) {
        CHECK( tool.type == itype_3d_printer_advanced );
    }
}

TEST_CASE( "carbon_fiber_salvages_and_repairs_with_filament", "[material][3d_printing]" )
{
    if( !printing_mod_loaded() ) {
        return;
    }
    CHECK( material_carbonfiber->salvaged_into() == itype_carbon_fiber_filament );
    CHECK( material_carbonfiber->repaired_with() == itype_carbon_fiber_filament );
    CHECK( item( itype_3d_printer_basic ).get_use( "repair_metal" ) != nullptr );
    CHECK( item( itype_3d_printer_advanced ).get_use( "repair_metal" ) != nullptr );
}

static vehicle *vehicle_with_rig( map &here, const tripoint_bub_ms &pos, const vpart_id &rig )
{
    vehicle *veh = here.add_vehicle( vehicle_prototype_none, pos, 0_degrees, 0, 0 );
    REQUIRE( veh != nullptr );
    REQUIRE( veh->install_part( here, point_rel_ms::zero, vpart_frame ) != -1 );
    REQUIRE( veh->install_part( here, point_rel_ms::zero, vpart_small_storage_battery ) != -1 );
    REQUIRE( veh->install_part( here, point_rel_ms::zero, rig ) != -1 );
    veh->refresh();
    here.add_vehicle_to_cache( veh );
    veh->charge_battery( here, 1000 );
    return veh;
}

TEST_CASE( "mounted_printers_craft_and_repair_from_vehicle_power", "[vehicle][3d_printing]" )
{
    if( !printing_mod_loaded() ) {
        return;
    }
    const std::vector<std::pair<vpart_id, itype_id>> rigs = {
        { vpart_3d_printer_basicrig, itype_3d_printer_basic },
        { vpart_3d_printer_advancedrig, itype_3d_printer_advanced },
    };
    for( const auto &[rig, printer] : rigs ) {
        CAPTURE( rig.str() );
        clear_map();
        clear_vehicles();
        clear_avatar();
        map &here = get_map();
        avatar &player = get_avatar();
        const tripoint_bub_ms veh_pos( 60, 60, 0 );
        player.setpos( here, veh_pos + tripoint_rel_ms::north );
        vehicle *veh = vehicle_with_rig( here, veh_pos, rig );

        player.invalidate_crafting_inventory();
        const inventory &crafting = player.crafting_inventory();
        REQUIRE( crafting.count_item( printer ) == 1 );
        const item &pseudo = crafting.find_item( crafting.position_by_type( printer ) );
        CHECK( pseudo.ammo_remaining() > 0 );

        player.activity = player_activity( ACT_REPAIR_ITEM );
        player.activity.str_values.emplace_back( "repair_metal" );
        REQUIRE( vehicle::use_vehicle_tool( *veh, &here, veh_pos, printer, true ) );
        CHECK( player.activity.index == INT_MIN );
        REQUIRE( player.activity.str_values.size() == 2 );
        CHECK( player.activity.str_values.back() == printer.str() );
        player.activity = player_activity();
    }
}

// Filament is counted by charges, so item groups must give it as "charges": a "count" would
// spawn that many full 50-unit spools.
TEST_CASE( "filament_spawns_in_sensible_amounts", "[item_group][3d_printing]" )
{
    if( !printing_mod_loaded() ) {
        return;
    }
    for( const char *group : {
             "3d_printing_raw_materials", "robofac_3d_printing", "science", "chem_school",
             "supplies_reagents_lab", "ig_vp_carbon"
         } ) {
        CAPTURE( group );
        Item_spawn_data *spawn = item_controller->get_group( item_group_id( group ) );
        REQUIRE( spawn != nullptr );
        const auto bounds = spawn->every_item_min_max();
        const auto found = bounds.find( &*itype_carbon_fiber_filament );
        REQUIRE( found != bounds.end() );
        CHECK( found->second.second <= 100 );
    }
}

static units::mass heaviest_debris( const item_group_id &group )
{
    units::mass total = 0_gram;
    Item_spawn_data *spawn = item_controller->get_group( group );
    if( spawn == nullptr ) {
        return total;
    }
    for( const auto &[type, min_max] : spawn->every_item_min_max() ) {
        total += type->weight * min_max.second;
    }
    return total;
}

// Wrecking a printer, rig or carbon fiber part must not leave more material than it was made of
TEST_CASE( "printing_vehicle_parts_break_into_no_more_than_they_weigh", "[vehicle][3d_printing]" )
{
    if( !printing_mod_loaded() ) {
        return;
    }
    for( const char *id : {
             "3d_printer_basicrig", "3d_printer_advancedrig", "ap_3d_printer_basic", "ap_3d_printer_advanced",
             "frame_carbon", "trunk_carbon", "trunk_floor_carbon", "cargo_space_carbon",
             "cargo_space_carbon_external", "carbon_board", "carbon_halfboard", "carbon_stowboard",
             "plating_carbon"
         } ) {
        const vpart_id part( id );
        REQUIRE( part.is_valid() );
        const units::mass debris = heaviest_debris( part->breaks_into_group );
        const units::mass weight = part->base_item->weight;
        CAPTURE( id, units::to_gram( debris ), units::to_gram( weight ) );
        CHECK( debris <= weight );
    }
}

// Filament in an item: what its cheapest printer recipe uses, counting printed components
// such as the carbon fiber sheets in a floor trunk
static int filament_in( const itype_id &type, std::map<itype_id, int> &memo, int depth = 0 )
{
    if( type == itype_carbon_fiber_filament ) {
        return 1;
    }
    const auto known = memo.find( type );
    if( known != memo.end() ) {
        return known->second;
    }
    int cheapest = 0;
    bool printed = false;
    if( depth < 4 ) {
        for( const auto &[id, r] : recipe_dict ) {
            if( r.obsolete || r.is_blacklisted() || r.result() != type || !uses_printer( r ) ) {
                continue;
            }
            int filament = 0;
            for( const std::vector<item_comp> &alternatives : r.simple_requirements().get_components() ) {
                int most = 0;
                for( const item_comp &comp : alternatives ) {
                    most = std::max( most, filament_in( comp.type, memo, depth + 1 ) * comp.count );
                }
                filament += most;
            }
            filament /= std::max( 1, r.makes_amount() );
            cheapest = printed ? std::min( cheapest, filament ) : filament;
            printed = true;
        }
    }
    memo[type] = cheapest;
    return cheapest;
}

static int filament_on_ground( map &here, const tripoint_bub_ms &center )
{
    int filament = 0;
    for( const tripoint_bub_ms &p : here.points_in_radius( center, 1 ) ) {
        for( const item &it : here.i_at( p ) ) {
            if( it.typeId() == itype_carbon_fiber_filament ) {
                filament += it.charges;
            }
        }
    }
    return filament;
}

// Salvaging a print, even one found in the world, gives back no more filament than printing it takes
TEST_CASE( "salvaging_prints_returns_no_more_filament_than_they_take", "[salvage][3d_printing]" )
{
    if( !printing_mod_loaded() ) {
        return;
    }
    std::set<itype_id> prints;
    for( const auto &[id, r] : recipe_dict ) {
        if( !r.obsolete && !r.is_blacklisted() && uses_printer( r ) ) {
            prints.insert( r.result() );
        }
    }
    std::map<itype_id, int> memo;

    clear_map();
    clear_avatar();
    map &here = get_map();
    avatar &player = get_avatar();
    const tripoint_bub_ms spot = player.pos_bub();
    const salvage_actor salvage;
    item cutter( itype_knife_combat );
    int checked = 0;
    for( const itype_id &type : prints ) {
        const int needed = filament_in( type, memo );
        item print( type );
        if( needed == 0 || !print.is_salvageable() || print.count_by_charges() ) {
            continue;
        }
        ++checked;
        CAPTURE( type.str(), needed );
        for( const tripoint_bub_ms &p : here.points_in_radius( spot, 1 ) ) {
            here.i_clear( p );
        }
        item &placed = here.add_item( spot, print );
        item_location loc( map_cursor( spot ), &placed );
        REQUIRE( salvage.try_to_cut_up( player, cutter, loc ) );
        CHECK( filament_on_ground( here, spot ) <= needed );
    }
    CHECK( checked > 20 );
}
