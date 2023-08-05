from HinetPy import Client

client = Client("seisman", "seismanustc")
client.get_event_waveform('201001010000', '201001020000',
                          minmagnitude=4.0, maxmagnitude=7.0,
                          mindepth=0, maxdepth=70)
