#include "math_parser_lex.h"

#include <cctype>
#include <clocale>
#include <cstddef>
#include <functional>
#include <locale>
#include <string>
#include <string_view>
#include <vector>

#include "cata_scope_helpers.h"
#include "math_parser_type.h"

namespace
{
// The <cctype> functions take an unsigned char value. A byte of a UTF-8
// sequence is a negative char, which is undefined behaviour (and aborts on
// NetBSD), so convert first.
bool ispunct( char c )
{
    return c != '_' && std::ispunct( static_cast<unsigned char>( c ) ) != 0;
}
bool is_space( char c )
{
    return std::isspace( static_cast<unsigned char>( c ) ) != 0;
}
bool is_digit( char c )
{
    return std::isdigit( static_cast<unsigned char>( c ) ) != 0;
}

} // namespace

namespace math
{

void lexer::skip( std::size_t n )
{
    str.remove_prefix( n );
}

void lexer::tokenize( token_t type, std::size_t n )
{
    ret.emplace_back( type, str.substr( 0, n ) );
    str.remove_prefix( n );
}

void lexer::read_number()
{
    std::size_t len = 0;
    bool have_dot = false;
    bool have_exp = false;

    while( len < str.size() ) {
        char const next = str[len];
        if( is_digit( next ) ) {
            len++;
        } else if( next == '.' && !have_dot && !have_exp ) {
            have_dot = true;
            len++;
        } else if( ( next == 'e' || next == 'E' ) && !have_exp ) {
            have_exp = true;
            len++;
            if( str.size() > len && ( str[len] == '+' || str[len] == '-' ) ) {
                len++;
            }
        } else {
            break;
        }
    }

    tokenize( token_t::number, len );
}

void lexer::read_string()
{
    skip( 1 );
    std::size_t len = 0;
    while( len < str.size() ) {
        char const next = str[len];
        if( next == '\'' && ( len == 0 || str[len - 1] != '\\' ) ) {
            break;
        }
        len++;
    }

    tokenize( token_t::string, len );
    if( str.empty() ) {
        throw math::syntax_error( "Unterminated string" );
    }
    skip( 1 );
}

void lexer::read_id()
{
    std::size_t len = 0;
    while( len < str.size() ) {
        char const next = str[len];
        if( ispunct( next ) || is_space( next ) ) {
            break;
        }
        len++;
    }
    tokenize( token_t::id, len );
}

lexer::lexer( std::string_view str_ ) : str( str_ )
{
    std::locale const &oldloc = std::locale();
    on_out_of_scope reset_loc( [&oldloc]() {
        std::locale::global( oldloc );
        char *discard [[maybe_unused]] = std::setlocale( LC_ALL, oldloc.name().c_str() );
    } );

    while( !str.empty() ) {
        char const next = str.front();

        if( str.size() == 2 && ( str == "++" || str == "--" ) ) {
            tokenize( token_t::oper, 2 );

        } else if( is_space( next ) ) {
            skip( 1 );

        } else if( is_digit( next ) ||
                   ( str.size() >= 2 && next == '.' && is_digit( str[1] ) ) ) {
            read_number();

        } else if( next == '>' || next == '<' || next == '!' || next == '+' || next == '-' ||
                   next == '*' || next == '/' || next == '%' || next == '=' ) {
            if( str.size() >= 2 && str[1] == '=' ) {
                tokenize( token_t::oper, 2 );
            } else {
                tokenize( token_t::oper, 1 );
            }

        } else if( next == '\'' ) {
            read_string();

        } else if( ispunct( next ) ) {
            tokenize( token_t::oper, 1 );

        } else {
            read_id();
        }
    }
}

std::vector<token> const &lexer::tokens()
{
    return ret;
}

} // namespace math
