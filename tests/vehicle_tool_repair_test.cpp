#include <climits>
#include <string>

#include "activity_type.h"
#include "avatar.h"
#include "calendar.h"
#include "cata_catch.h"
#include "coordinates.h"
#include "item.h"
#include "itype.h"
#include "map.h"
#include "map_helpers.h"
#include "player_activity.h"
#include "player_helpers.h"
#include "point.h"
#include "type_id.h"
#include "units.h"
#include "vehicle.h"
#include "vpart_position.h"

static const activity_id ACT_REPAIR_ITEM( "ACT_REPAIR_ITEM" );

static const itype_id itype_welder( "welder" );

static const vpart_id vpart_frame( "frame" );
static const vpart_id vpart_small_storage_battery( "small_storage_battery" );
static const vpart_id vpart_veh_tools_workshop( "veh_tools_workshop" );

static const vproto_id vehicle_prototype_none( "none" );

// Using a repair tool mounted on a vehicle hands the repair activity a pseudo item that
// draws on the vehicle's batteries; the activity finds it through these markers.
TEST_CASE( "mounted_repair_tool_marks_repair_activity", "[vehicle][repair]" )
{
    clear_map();
    clear_vehicles();
    clear_avatar();
    map &here = get_map();
    avatar &player = get_avatar();
    const tripoint_bub_ms veh_pos( 60, 60, 0 );
    player.setpos( here, veh_pos + tripoint_rel_ms::north );

    vehicle *veh = here.add_vehicle( vehicle_prototype_none, veh_pos, 0_degrees, 0, 0 );
    REQUIRE( veh != nullptr );
    REQUIRE( veh->install_part( here, point_rel_ms::zero, vpart_frame ) != -1 );
    REQUIRE( veh->install_part( here, point_rel_ms::zero, vpart_small_storage_battery ) != -1 );
    const int workshop_idx = veh->install_part( here, point_rel_ms::zero, vpart_veh_tools_workshop );
    REQUIRE( workshop_idx != -1 );
    veh->refresh();
    here.add_vehicle_to_cache( veh );
    veh->get_tools( veh->part( workshop_idx ) ).emplace_back( itype_welder, calendar::turn );
    veh->charge_battery( here, 1000 );

    player.activity = player_activity( ACT_REPAIR_ITEM );
    // As repair_item_actor::use starts it: the first string names the repair action
    player.activity.str_values.emplace_back( "repair_metal" );
    REQUIRE( itype_welder->can_use( "repair_metal" ) );
    REQUIRE( vehicle::use_vehicle_tool( *veh, &here, veh_pos, itype_welder, true ) );

    CHECK( player.activity.index == INT_MIN );
    REQUIRE( !player.activity.coords.empty() );
    CHECK( player.activity.coords.back() == here.get_abs( veh_pos ) );
    REQUIRE( player.activity.str_values.size() == 2 );
    CHECK( player.activity.str_values.back() == itype_welder.str() );
    player.activity = player_activity();
}
