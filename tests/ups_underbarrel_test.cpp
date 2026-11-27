#include <vector>

#include "avatar.h"
#include "calendar.h"
#include "character_attire.h"
#include "cata_catch.h"
#include "coordinates.h"
#include "item.h"
#include "item_location.h"
#include "map.h"
#include "map_helpers.h"
#include "player_helpers.h"
#include "pocket_type.h"
#include "point.h"
#include "ret_val.h"
#include "type_id.h"
#include "units.h"

static const itype_id itype_UPS_off( "UPS_off" );
static const itype_id itype_afs_coilgun_underbarrel( "afs_coilgun_underbarrel" );
static const itype_id itype_debug_backpack( "debug_backpack" );
static const itype_id itype_heavy_plus_battery_cell( "heavy_plus_battery_cell" );
static const itype_id itype_nail( "nail" );
static const itype_id itype_scar_l( "scar_l" );
static const itype_id itype_test_ups_underbarrel( "test_ups_underbarrel" );

// Fire an underbarrel gun that runs on a UPS, and check the shot uses its ammo and the UPS
static void check_ups_underbarrel_fires( const itype_id &underbarrel )
{
    clear_map();
    clear_avatar();
    map &here = get_map();
    avatar &shooter = get_avatar();

    shooter.worn.wear_item( shooter, item( itype_debug_backpack ), false, false );
    item ups( itype_UPS_off );
    item cell( itype_heavy_plus_battery_cell );
    cell.ammo_set( cell.ammo_default() );
    REQUIRE( ups.put_in( cell, pocket_type::MAGAZINE_WELL ).success() );
    shooter.i_add( ups );

    item rifle( itype_scar_l );
    REQUIRE( rifle.put_in( item( underbarrel ), pocket_type::MOD ).success() );
    REQUIRE( shooter.wield( rifle ) );
    item_location wielded = shooter.get_wielded_item();
    REQUIRE( wielded );

    item *found = nullptr;
    for( item *gunmod : wielded->gunmods() ) {
        if( gunmod->typeId() == underbarrel ) {
            found = gunmod;
        }
    }
    REQUIRE( found != nullptr );
    item &mod = *found;
    item_location nails = shooter.i_add( item( itype_nail, calendar::turn, 5 ) );
    REQUIRE( nails );
    REQUIRE( mod.reload( shooter, nails, 5 ) );
    REQUIRE( mod.ammo_remaining() == 5 );

    const units::energy drain = mod.get_gun_energy_drain();
    REQUIRE( drain > 0_kJ );
    const units::energy ups_before = shooter.available_ups();
    REQUIRE( ups_before >= drain );
    CHECK( mod.shots_remaining( here, &shooter ) > 0 );

    const tripoint_bub_ms target = shooter.pos_bub() + tripoint_rel_ms( 5, 0, 0 );
    CHECK( shooter.fire_gun( here, target, 1, mod ) == 1 );
    CHECK( mod.ammo_remaining() == 4 );
    CHECK( shooter.available_ups() == ups_before - drain );
}

TEST_CASE( "ups_powered_underbarrel_gun_fires_from_ups", "[gun][gunmod][ups]" )
{
    SECTION( "test underbarrel gun" ) {
        check_ups_underbarrel_fires( itype_test_ups_underbarrel );
    }
    // Aftershock's underbarrel coilgun, when the mod is loaded
    if( itype_afs_coilgun_underbarrel.is_valid() ) {
        SECTION( "underbarrel coilgun" ) {
            check_ups_underbarrel_fires( itype_afs_coilgun_underbarrel );
        }
    }
}
