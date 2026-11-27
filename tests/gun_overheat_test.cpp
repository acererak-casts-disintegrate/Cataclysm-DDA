#include <string>
#include <utility>
#include <vector>

#include "calendar.h"
#include "cata_catch.h"
#include "character.h"
#include "item.h"
#include "map_helpers.h"
#include "player_helpers.h"
#include "ret_val.h"
#include "type_id.h"

static const fault_id fault_overheat_melting( "fault_overheat_melting" );
static const fault_id fault_test_fault_overheat_melting( "test_fault_overheat_melting" );

static const itype_id itype_test_overheating_gun( "test_overheating_gun" );
static const itype_id itype_test_overheating_gun_core_fault( "test_overheating_gun_core_fault" );

// Overheat a gun until it melts, and return whether it did within a generous number of tries
static bool overheat_until_melted( Character &shooter, item &gun )
{
    for( int i = 0; i < 200; ++i ) {
        gun.set_var( "gun_heat", 100.0 );
        shooter.handle_gun_overheat( gun );
        if( gun.has_fault_flag( "RUINED_GUN" ) ) {
            return true;
        }
    }
    return false;
}

TEST_CASE( "overheating_melts_a_gun_with_the_melting_fault_it_lists", "[gun][overheat]" )
{
    clear_avatar();
    Character &shooter = get_player_character();
    const std::vector<std::pair<itype_id, fault_id>> cases = {
        { itype_test_overheating_gun, fault_test_fault_overheat_melting },
        { itype_test_overheating_gun_core_fault, fault_overheat_melting }
    };
    for( const std::pair<itype_id, fault_id> &c : cases ) {
        CAPTURE( c.first.str() );
        item gun( c.first );
        REQUIRE( overheat_until_melted( shooter, gun ) );
        CHECK( gun.has_fault( c.second ) );
        CHECK( gun.faults.size() == 1 );
    }
}

TEST_CASE( "guns_with_fused_internals_cannot_be_disassembled", "[gun][overheat][disassembly]" )
{
    clear_avatar();
    clear_map();
    set_time( calendar::turn_zero + 12_hours );
    Character &player_character = get_player_character();
    item gun( itype_test_overheating_gun );
    REQUIRE( player_character.can_disassemble( gun, player_character.crafting_inventory() ).success() );

    gun.set_fault( fault_test_fault_overheat_melting );
    const ret_val<void> refused = player_character.can_disassemble( gun,
                                  player_character.crafting_inventory() );
    CHECK_FALSE( refused.success() );
    CHECK( refused.str() == "Its internals have fused together.  It can only be mended." );
}
