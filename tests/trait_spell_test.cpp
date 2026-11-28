#include <string>

#include "avatar.h"
#include "cata_catch.h"
#include "debug.h"
#include "magic.h"
#include "pimpl.h"
#include "player_helpers.h"
#include "type_id.h"

static const spell_id spell_test_spell_trait_shared( "test_spell_trait_shared" );

static const trait_id trait_spell_source_test_1( "spell_source_test_1" );
static const trait_id trait_spell_source_test_2( "spell_source_test_2" );
static const trait_id trait_spell_source_test_3( "spell_source_test_3" );

// Mind Over Matter gives every psionic path the same concentration spells at level 1, and each
// trait granting them adds its levels on top, past the spell's max_level.  Losing one of those
// traits must take away only its own levels.
TEST_CASE( "losing_one_of_several_traits_keeps_their_shared_spell", "[magic][spell][mutation]" )
{
    avatar &u = get_avatar();
    clear_avatar();
    const std::string msgs = capture_debugmsg_during( [&u]() {
        u.toggle_trait( trait_spell_source_test_1 );
        u.toggle_trait( trait_spell_source_test_2 );
        u.toggle_trait( trait_spell_source_test_3 );
        REQUIRE( u.magic->knows_spell( spell_test_spell_trait_shared ) );
        CHECK( u.magic->get_spell( spell_test_spell_trait_shared ).get_level() == 3 );

        u.toggle_trait( trait_spell_source_test_3 );
        REQUIRE( u.magic->knows_spell( spell_test_spell_trait_shared ) );
        CHECK( u.magic->get_spell( spell_test_spell_trait_shared ).get_level() == 2 );

        u.toggle_trait( trait_spell_source_test_2 );
        REQUIRE( u.magic->knows_spell( spell_test_spell_trait_shared ) );
        CHECK( u.magic->get_spell( spell_test_spell_trait_shared ).get_level() == 1 );

        u.toggle_trait( trait_spell_source_test_1 );
        CHECK_FALSE( u.magic->knows_spell( spell_test_spell_trait_shared ) );
    } );
    CHECK( msgs.empty() );
}

TEST_CASE( "losing_a_trait_whose_spell_is_already_forgotten", "[magic][spell][mutation]" )
{
    avatar &u = get_avatar();
    clear_avatar();
    u.toggle_trait( trait_spell_source_test_1 );
    REQUIRE( u.magic->knows_spell( spell_test_spell_trait_shared ) );
    u.magic->forget_spell( spell_test_spell_trait_shared );

    const std::string msgs = capture_debugmsg_during( [&u]() {
        u.toggle_trait( trait_spell_source_test_1 );
    } );
    CHECK_FALSE( u.has_trait( trait_spell_source_test_1 ) );
    CHECK( msgs.empty() );
}
