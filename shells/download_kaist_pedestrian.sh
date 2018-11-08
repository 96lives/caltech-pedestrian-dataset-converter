
if [ ! -d data ]; then
    mkdir data
fi
if [ ! -d data/kaist_pedestrian ]; then
    mkdir data/kaist_pedestrian
fi
cd data/kaist_pedestrian

# get annotations
wget http://multispectral.kaist.ac.kr/pedestrian/data-kaist/annotations.tar
tar -xvf annotations
mv annotations vbb
rm -rf annotations.tar




