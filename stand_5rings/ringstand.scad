// NeoPixel ring mount
// this is a pure 2d design...

// DEBUG
//$fn = 120; // while editing..
$fn = 720; // big object, needs lots of lines, slow


// Note; the following is sized for my rings
// which sit under a 240mm plastic diffuser.
ringdia = 125;  // outer ring diameter (plus allowance)
lugs = 3;       // number of lugs
lugwide = 16;   // lug width

outdia = 244;   // total diameter (plus allowance)
outwide = 20;   // outer ring width

// Calculate the angle between each lug
lugangle = 360 / lugs;

// center
module center() {
    union() {
        circle(d=ringdia);
        for (r=[0:lugangle:360]) {
            rotate([0,0,r])
            translate([0,-lugwide/2])
            square([(ringdia/2)+lugwide,lugwide]);
        }
        translate([-(ringdia/2)-lugwide,-lugwide/2])
        square([(ringdia/2)+lugwide,lugwide]);
    }
}

// Outer
module ring() rotate(lugangle/4){
   union() {
        difference() {
            circle(d=outdia);
            circle(d=outdia-(2*outwide));
        }
        for (r=[0:lugangle:360]) {
            rotate([0,0,r])
            translate([ringdia/2+1,-lugwide/2])
            square([((outdia/2)-outwide)-(ringdia/2),lugwide]);
        }
    }
}

// Now render the two together, and use a
// seriously inneficient ugly hack to round them off.
color("olive",0.5)
offset(r=2) offset(delta=-2)
offset(r=-2) offset(delta=2) 
ring();
color("peru",0.5)
offset(r=2) offset(delta=-2)
offset(r=-2) offset(delta=2) 
center();

// support 'pillars' (3x3, plus 1 spare)
for (r=[15,0,-15,-30,-45]) {
    rotate(r)
    for (y=[72,90]) {
        translate([0,y])
        minkowski() {
            square([lugwide-4, lugwide-4],center=true);
            circle(2);
        }
    }
}

// Infill pieces to support lightring
// while allowing space under them for wires
translate([-79,-23])
rotate(-60)
for (x=[-12, 0, 12]) {
    translate([0,x]) 
    hull() {
        circle(d=10);
        rotate(-x/1.5) translate([45,0]) circle(d=4);
    }
}