chmod +x gen.sh
./gen.sh
TV08Scorer --showAT --allAT --writexml output/xml/ --pruneEvents --computeDETCurve --OutputFileRoot output --titleOfSys "sed" --observationCont --ecf template/TRECVid08_ecf_v2/ecf.xml xml/*.xml  --gtf gtf_xml/*.xml --fps 25 --deltat 10 --limitto CellToEar,Embrace,Pointing --MissCost 10 --CostFA 1 --Rtarget 20
