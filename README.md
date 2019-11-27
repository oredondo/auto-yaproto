# auto-yaproto
/usr/bin/make -f /vagrant/data/yaproto/Makefile all


java -Djava.library.path=/vagrant/data/yaproto/lib  -classpath /vagrant/data/yaproto/lib/slf4j-api-1.6.6.jar:/vagrant/data/yaproto/lib/slf4j-jdk14-1.6.6.jar:/vagrant/data/yaproto/bin msti.ospfv2.SimuladorEncaminadorOSPFv2

java -Djava.library.path=/vagrant/data/yaproto/lib  -classpath /vagrant/data/yaproto/lib/slf4j-api-1.6.6.jar:/vagrant/data/yaproto/lib/slf4j-jdk14-1.6.6.jar:/vagrant/data/yaproto/bin msti.rip.SimuladorEncaminadorRIPv2



jni.cc=gcc -I/usr/lib/jvm/java-1.6.0-openjdk-1.6.0.41.x86_64/include -I/usr/lib/jvm/java-1.6.0-openjdk-1.6.0.41.x86_64/include/linux -nostartfiles

Install gcc and wget
# download and install
antversion=1.9.13
wget http://archive.apache.org/dist/ant/binaries/apache-ant-${antversion}-bin.tar.gz
sudo tar xvfvz apache-ant-${antversion}-bin.tar.gz -C /opt
sudo ln -sfn /opt/apache-ant-${antversion} /opt/ant
sudo sh -c 'echo ANT_HOME=/opt/ant >> /etc/environment'
sudo ln -sfn /opt/ant/bin/ant /usr/bin/ant

# check installation
ant -version

#cleanup
rm apache-ant-${antversion}-bin.tar.gz

ant -Djni.cc='gcc -m64'
ant -Djni.cc='gcc -m64 -I/usr/lib/jvm/java-1.8.0/include -I/usr/lib/jvm/java-1.8.0/include/linux -Wall'


ant jar
