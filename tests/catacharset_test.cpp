#include <clocale>
#include <functional>
#include <locale>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "cata_catch.h"
#include "catacharset.h"
#include "localized_comparator.h"
#include "unicode.h"

TEST_CASE( "utf8_width", "[catacharset][nogame]" )
{
    CHECK( utf8_width( "Hello, world!", false ) == 13 );
    CHECK( utf8_width( "你好，世界！", false ) == 12 );
    CHECK( utf8_width( "Hello, 世界!", false ) == 12 );
    CHECK( utf8_width( "<color_green>激活</color>", true ) == 4 );
    CHECK( utf8_width( "<color_green>激活</color>", false ) == 25 );
    CHECK( utf8_width( "à", false ) == 1 );
    CHECK( utf8_width( "y\u0300", false ) == 1 );
    CHECK( utf8_width( "à̸̠你⃫", false ) == 3 );
}

TEST_CASE( "utf8_display_split", "[catacharset][nogame]" )
{
    CHECK( utf8_display_split( "你好" ) == std::vector<std::string> { "你", "好" } );
    CHECK( utf8_display_split( "à" ) == std::vector<std::string> { "à" } );
    CHECK( utf8_display_split( "y\u0300" ) == std::vector<std::string> { "y\u0300" } );
    CHECK( utf8_display_split( "à̸̠你⃫" ) == std::vector<std::string> { "à̸̠", "你⃫" } );
    CHECK( utf8_display_split( "    " ) == std::vector<std::string> { " ", " ", " ", " " } );
}

TEST_CASE( "base64", "[catacharset][nogame]" )
{
    CHECK( base64_encode( "hello" ) == "#aGVsbG8=" );
    CHECK( base64_decode( "#aGVsbG8=" ) == "hello" );
}

TEST_CASE( "utf8_to_wstr", "[catacharset][nogame]" )
{
    // std::mbstowcs' returning -1 workaround
    char *result = setlocale( LC_ALL, "" );
    REQUIRE( result );
    std::string src( u8"Hello, 世界!" );
    std::wstring dest( L"Hello, 世界!" );
    CHECK( utf8_to_wstr( src ) == dest );
    result = setlocale( LC_ALL, "C" );
    REQUIRE( result );
}

TEST_CASE( "wstr_to_utf8", "[catacharset][nogame]" )
{
    // std::wcstombs' returning -1 workaround
    char *result = setlocale( LC_ALL, "" );
    REQUIRE( result );
    std::wstring src( L"Hello, 世界!" );
    std::string dest( u8"Hello, 世界!" );
    CHECK( wstr_to_utf8( src ) == dest );
    result = setlocale( LC_ALL, "C" );
    REQUIRE( result );
}

TEST_CASE( "localized_compare", "[catacharset][nogame]" )
{
    try {
        std::locale::global( std::locale( "en_US.UTF-8" ) );
    } catch( std::runtime_error & ) {
        // On platforms where we can't set the locale, ignore this test
        return;
    }
    CAPTURE( setlocale( LC_ALL, nullptr ) );
    CAPTURE( std::locale().name() );
    // Some C libraries (NetBSD's, OpenBSD's) accept the locale but still collate
    // byte by byte, so "B" sorts before "a" and there is no localized ordering to
    // test.
    if( std::locale()( std::string( "B" ), std::string( "a" ) ) ) {
        WARN( "This platform's en_US.UTF-8 locale does not collate by locale; skipping." );
        std::locale::global( std::locale::classic() );
        return;
    }
    std::string a = "a";
    std::string b = "b";
    std::string c = "c";
    std::string A = "A";
    std::string B = "B";
    CHECK( !localized_compare( a, a ) );
    CHECK( localized_compare( a, B ) );
    CHECK( localized_compare( A, b ) );
    CHECK( !localized_compare( B, a ) );
    CHECK( !localized_compare( b, A ) );
    CHECK( localized_compare( std::make_pair( a, a ), std::make_pair( a, B ) ) );
    CHECK( localized_compare( std::make_tuple( a ), std::make_tuple( B ) ) );
    CHECK( localized_compare( std::make_tuple( a, c, c ), std::make_tuple( B, a, a ) ) );
    CHECK( localized_compare( std::make_tuple( a, a, c ), std::make_tuple( a, B, a ) ) );
    CHECK( localized_compare( std::make_tuple( a, a, a ), std::make_tuple( a, a, B ) ) );
    std::locale::global( std::locale::classic() );
}

static void check_in_place_func( const std::function<void( char32_t & )> &func,
                                 char32_t ch, char32_t expected )
{
    func( ch );
    CHECK( ch == expected );
}

TEST_CASE( "u32_to_lowercase", "[catacharset][nogame]" )
{
    // Latin
    check_in_place_func( u32_to_lowercase, U'a', U'a' );
    check_in_place_func( u32_to_lowercase, U'A', U'a' );
    check_in_place_func( u32_to_lowercase, U'é', U'é' );
    check_in_place_func( u32_to_lowercase, U'É', U'é' );
    check_in_place_func( u32_to_lowercase, U'ō', U'ō' );
    check_in_place_func( u32_to_lowercase, U'Ō', U'ō' );

    // Cyrillic
    check_in_place_func( u32_to_lowercase, U'а', U'а' );
    check_in_place_func( u32_to_lowercase, U'А', U'а' );
    check_in_place_func( u32_to_lowercase, U'б', U'б' );
    check_in_place_func( u32_to_lowercase, U'Б', U'б' );

    // CJK
    check_in_place_func( u32_to_lowercase, U'中', U'中' );
    check_in_place_func( u32_to_lowercase, U'の', U'の' );

    // Emoji
    check_in_place_func( u32_to_lowercase, U'😅', U'😅' );
}

TEST_CASE( "remove_accent", "[catacharset][nogame]" )
{
    // Latin
    check_in_place_func( remove_accent, U'o', U'o' );
    check_in_place_func( remove_accent, U'ô', U'o' );
    check_in_place_func( remove_accent, U'ö', U'o' );
    check_in_place_func( remove_accent, U'ō', U'o' );

    // Cyrillic
    check_in_place_func( remove_accent, U'б', U'б' );

    // CJK
    check_in_place_func( remove_accent, U'中', U'中' );
    check_in_place_func( remove_accent, U'の', U'の' );

    // Emoji
    check_in_place_func( remove_accent, U'😅', U'😅' );
}

TEST_CASE( "utf8_view", "[catacharset][nogame]" )
{
    static const std::string str{"Français中文русский"};
    static const std::vector<char32_t> expected_code_points{
        0x46, 0x72, 0x61, 0x6e, 0xe7, 0x61, 0x69, 0x73, // Latin
        0x4e2d, 0x6587, // CJK
        0x440, 0x443, 0x441, 0x441, 0x43a, 0x438, 0x439 // Cyrillic
    };
    std::vector<char32_t> actual_code_points;
    for( char32_t c : utf8_view( str ) ) {
        actual_code_points.emplace_back( c );
    }
    CHECK( actual_code_points == expected_code_points );
}

