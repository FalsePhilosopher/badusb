#!/usr/bin/gawk -f

BEGIN {
  mode = 1;
}

function output_glyph(_, tail, offset, len, i, j, x, y, l, bit_j) {
  tail = head;
  offset = 0;
  while (match(tail, /^[^[:space:]]+/) > 0) {
    len = RLENGTH;

    c = substr(tail, 1, RLENGTH);
    if (c ~ /^U\+.*$/) {
      c = "00000000" substr(c, 3);
      c = "\\U" substr(c, length(c) - 7);
    } else if (c ~ /^[\\\']/) {
      c = "\\" substr(c, 1, 1);
    } else {
      c = substr(c, 1, 1);
    }
    printf("{U'%s', %d, {", c, len);

    for (i = 0; i < 7; i++) {
      x = substr(data[i], offset + 1, len);
      l = length(x);
      y = 0;
      bit_j = 1;
      for (j = 0; j < l; j++) {
        if (substr(x, j + 1, 1) ~ /[^[:space:]]/) {
          y += bit_j;
        }
        bit_j *= 2;
      }
      printf("%d, ", y);
    }
    printf("}},\n");

    match(tail, /^[^[:space:]]+[[:space:]]*/);
    offset += RLENGTH;
    tail = substr(tail, RLENGTH + 1);
  }
}

mode == 1 {
  if (/^[[:space:]]*(#|$)/) next;

  mode = 2;
  head = $0;
  iline = 0;
  next;
}

mode == 2 {
  if (/^[[:space:]]*$/) next;

  data[iline++] = $0
  if (iline == 7) {
    output_glyph();
    mode = 1;
  }
  next;
}
