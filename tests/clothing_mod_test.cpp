#include "cata_catch.h"
#include "clothing_mod.h"
#include "item.h"
#include "type_id.h"

static const clothing_mod_id clothing_mod_leather_padded( "leather_padded" );

static const itype_id itype_tshirt( "tshirt" );

TEST_CASE( "clothing_mod_values_scale_with_fractional_thickness", "[item][clothing_mod]" )
{
    const item shirt( itype_tshirt );
    const float thickness = shirt.get_thickness();
    REQUIRE( thickness > 0.0f );
    REQUIRE( thickness < 1.0f );

    const clothing_mod &padding = clothing_mod_leather_padded.obj();
    // Protection scales with the garment's thickness, so a thin garment gets a fraction of it
    CHECK( padding.get_mod_val( clothing_mod_type_bash, shirt ) == Approx( thickness ) );
    CHECK( padding.get_mod_val( clothing_mod_type_cut, shirt ) == Approx( thickness ) );
    CHECK( padding.get_mod_val( clothing_mod_type_bullet, shirt ) == Approx( thickness ) );
    // Encumbrance rounds up, so padding a thin garment still costs something
    CHECK( padding.get_mod_val( clothing_mod_type_encumbrance, shirt ) == 1.0f );
}
