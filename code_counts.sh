#!/bin/bash
python_counts=`find . -name "*.py" | xargs cat | wc -l`
html_counts=`find . -name "*.html" | xargs cat | wc -l`
txt_counts=`find . -name "*.txt" | xargs cat | wc -l`
css_counts=`find . -name "*.css" | xargs cat | wc -l`
sh_counts=`find . -name "*.sh" | xargs cat | wc -l`

echo '----- count code lines-----'
echo '*.py:' $python_counts
echo '*.html:' $html_counts
echo '*.txt:' $txt_counts
echo '*.css:' $css_counts
echo '*.sh:' $sh_counts

let "sum=$python_counts+$html_counts+$txt_counts+$css_counts+$sh_counts" 

echo 'total:' "$sum"


