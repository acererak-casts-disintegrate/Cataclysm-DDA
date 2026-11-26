#include <algorithm>
#include <climits>
#include <string>
#include <vector>

#include "activity_type.h"
#include "avatar.h"
#include "calendar.h"
#include "cata_catch.h"
#include "coordinates.h"
#include "inventory.h"
#include "item.h"
#include "itype.h"
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
#include "vehicle.h"
#include "vpart_position.h"

// Tests for the 3D Printing mod (data/mods/3D_Printing); they do nothing when it is not loaded.

static const activity_id ACT_REPAIR_ITEM( "ACT_REPAIR_ITEM" );

static const itype_id itype_3d_printer_advanced( "3d_printer_advanced" );
static const itype_id itype_3d_printer_basic( "3d_printer_basic" );
static const itype_id itype_carbon_fiber_filament( "carbon_fiber_filament" );

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

static bool uses_printer( const recipe &r )
{
    for( const std::vector<tool_comp> &alternatives : r.simple_requirements().get_tools() ) {
        for( const tool_comp &tool : alternatives ) {
            if( tool.type == itype_3d_printer_basic || tool.type == itype_3d_printer_advanced ) {
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
// components it can be printed from.  This also keeps salvaging a print from yielding more
// filament or scrap than went into it.
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
