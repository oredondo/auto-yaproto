# auto-yaproto
/usr/bin/make -f /vagrant/data/yaproto/Makefile all


java -Djava.library.path=/vagrant/data/yaproto/lib  -classpath /vagrant/data/yaproto/lib/slf4j-api-1.6.6.jar:/vagrant/data/yaproto/lib/slf4j-jdk14-1.6.6.jar:/vagrant/data/yaproto/bin msti.ospfv2.SimuladorEncaminadorOSPFv2

java -Djava.library.path=/vagrant/data/yaproto/lib  -classpath /vagrant/data/yaproto/lib/slf4j-api-1.6.6.jar:/vagrant/data/yaproto/lib/slf4j-jdk14-1.6.6.jar:/vagrant/data/yaproto/bin msti.rip.SimuladorEncaminadorRIPv2
