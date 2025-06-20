conda deactivate
conda env remove -n "metsamask" -y
conda create -n "metsamask" python=3.13 -y
conda activate "metsamask"
pip install -r req.txt
