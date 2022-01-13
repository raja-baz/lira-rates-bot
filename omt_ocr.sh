rm /tmp/bla.{jpg,txt} 2> /dev/null
curl -s https://www.omt.com.lb/$1 -o /tmp/bla.jpg 2>/dev/null
tesseract /tmp/bla.jpg /tmp/bla 2>/dev/null
