jack_capture -d 4 out.wav > /dev/null 2>&1
python groove.py out.wav
#python groove.py out.wav fasst
rm -f out.wav
