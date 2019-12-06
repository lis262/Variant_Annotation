* Dockerfile: commands to build the docker image that have VEP and plugins including LOFTEE.
* gnomad.v2.1.1.oe_lof.by_gene.txt: gnomad recommend to replace ExACpLI loss of
function intolerant score with observed/expected (oe) metric. Details is here: ^?https://macarthurlab.org/2018/10/17/gnomad-v2-1/. So I donwloaded the constrain
t file from gnomad and extract two columns (gene symbol and oe_lof).
* Dockerfile_v1: commands to build the docker image that have VEP and plugins in
cluding LOFTEE, replace ExACpLI with gnomad.
