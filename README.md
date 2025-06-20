# Metsamask
Metsamaski arvutus kaugseire andmete alusel

## Install

Installimine toimub järgmiste käskudega
```
conda create -n "metsamask" python=3.13 -y
conda activate "metsamask"
pip install -r req.txt
```

## Andmetöötlus

### Lidari andmed

Config.json failis tuleb määrata "lidar_laz_dir". Selles kataloogis on eeldatud, et laz failid on paigutatud aastate kaupa kataloogidesse. 
Näidis kataloogipuu:
```
["lidar_laz_dir"]|
 |- 2008_tava
 |  |- 51281
 |  |  |- 420382_2008_tava.laz
```

Andmetöötlus toimub EPK10T ruutude kaupa ning seetõttu on sellesse alamkataloogi pandud kokku kõik laz failid. Andmetöötluse käigus ei arvutata eraldi välja maapinna mudelit, selleks kasutatakse Maa- ja Ruumiameti poolt arvutatud 5 m maapinna kõrgusmudel: 

Nii lidari kui ka maapinna kõrguse mudeli saab alla laadida:

https://geoportaal.maaamet.ee/est/ruumiandmed/korgusandmed/laadi-korgusandmed-alla-p614.html

