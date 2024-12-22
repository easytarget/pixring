// feet for pixel ring
$fn=360;   // not fugly

for (r=[0,120,240]) {
    rotate(r) 
    translate([0,20,0])
    foot();
}

module foot() {
    linear_extrude(height=12,convexity=10) {
        difference() {
            circle(d=20);
            circle(d=5);
        }
    }
    translate([0,0,12])
    linear_extrude(height=12,convexity=10) {
        difference() {
            circle(d=20);
            circle(d=10);
        }
    }
    
}