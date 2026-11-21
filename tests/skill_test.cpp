#include <string>
#include <vector>

#include "calendar.h"
#include "cata_catch.h"
#include "character.h"
#include "options.h"
#include "options_helpers.h"
#include "player_helpers.h"
#include "skill.h"

static void set_all_skills_to_two( Character &guy )
{
    // Set every skill to two, so they can rust
    for( const Skill &skill : Skill::skills ) {
        INFO( skill.ident().str() );
        guy.set_skill_level( skill.ident(), 2 );
        REQUIRE( guy.get_skill_level( skill.ident() ) == 2.f );
        REQUIRE( guy.get_knowledge_level( skill.ident() ) == 2 );
        REQUIRE_FALSE( guy.get_skill_level_object( skill.ident() ).isRusty() );
    }
}

static void wait_three_days( Character &guy )
{
    for( int i = 0; i < to_seconds<int>( 3_days ); ++i ) {
        calendar::turn += 1_seconds;
        guy.update_body();
        if( calendar::once_every( 4_hours ) ) {
            // Don't starve
            guy.set_stored_kcal( guy.get_healthy_kcal() );
            // Clear thirst and fatigue
            guy.environmental_revert_effect();
            // And sleep deprivation
            guy.set_sleep_deprivation( 0 );
        }
    }
}

TEST_CASE( "skill_rust_occurs", "[character][skill]" )
{
    // Skill rust defaults to off on this branch; opt in to test the mechanic itself.
    override_option rust_on( "SKILL_RUST", "vanilla" );
    Character &guy = get_player_character();
    clear_avatar();

    set_all_skills_to_two( guy );
    wait_three_days( guy );

    // Ensure they have rusted
    for( const Skill &skill : Skill::skills ) {
        INFO( skill.ident().str() );
        // Rust is about 1% per day with a one day grace period
        CHECK( guy.get_skill_level( skill.ident() ) < 2.f );
        CHECK( guy.get_knowledge_level( skill.ident() ) == 2 );
        CHECK( guy.get_skill_level_object( skill.ident() ).isRusty() );
    }
}

TEST_CASE( "skill_rust_off_by_default", "[character][skill]" )
{
    REQUIRE( get_option<std::string>( "SKILL_RUST" ) == "off" );
    Character &guy = get_player_character();
    clear_avatar();

    set_all_skills_to_two( guy );
    wait_three_days( guy );

    // Ensure nothing has rusted
    for( const Skill &skill : Skill::skills ) {
        INFO( skill.ident().str() );
        CHECK( guy.get_skill_level( skill.ident() ) == 2.f );
        CHECK( guy.get_knowledge_level( skill.ident() ) == 2 );
        CHECK_FALSE( guy.get_skill_level_object( skill.ident() ).isRusty() );
    }
}
