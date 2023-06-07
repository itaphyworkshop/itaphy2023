# Setup your environment

source /usr/local/etc/phyworkshop.sh

source /home/phyworkshop_040/anaconda3/etc/profile.d/conda.sh

export PATH="/home/phyworkshop_040/tools/VSCode-linux-x64:$PATH"

conda env create -f environment.yml
