
var mm = [-2, 15, 1010, 1034];

function calc (data) {

  var diff1  = data[1] - data[0], diff2 = data[3] - data[2];
  var lines  = [2, 3, 4];
  var grids1 = [1, 2, 4, 5, 10], grids2 = [2, 5, 10, 20, 40];
  var sols1  = [], sols2  = [];
  
  lines.forEach(l => {
    grids1.forEach(g => {
      sols1.push([l, g, l * g]);
    });
  });
  
  var s1 = sols1.filter(s => s[2] > diff1).sort( (a, b) => a[2] > b[2] ? 1 : -1)[0];
  var lines1 = s1[0] +2;
  
  grids2.forEach( g => {
    sols2.push([g, g * lines1]);
  });
  
  var s2 = sols2.filter(s => s1 > diff1).sort( (a, b) => a[1] > b[1] ? 1 : -1)[0]
  
  return {
    sol1: s1,
    min1: s1[2] - (s1[0] + 1) * s1[1], 
    max1: s1[2] + s1[1],
    interval1: s1[1],
    sol2: s2,
    min1: NaN,
    max2: NaN,
    interval2: s2[1]
    lines: lines1
  }
  
}

JSON.stringify(calc(mm))

/*
{"sol":[3,5,15],"min":-5,"max":20,"grid":5,"lines":5}
*/
/*
{"sol":[2,10,20],"min":-10,"max":30,"grid":10,"lines":4}
*/