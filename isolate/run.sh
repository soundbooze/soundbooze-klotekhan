jack_capture -d 32 out.wav > /dev/null 2>&1
python isolate.py out.wav
#python groove.py out.wav fasst
rm -f out.wav
