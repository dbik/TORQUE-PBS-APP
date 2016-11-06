# TORQUE-PBS-APP
<h3>Restful web application, allows users to interact with Torque pbs over a WEB UI</h3>
<p>e.g. Submit, manage jobs and monitor cluster resources</p>
<p>The project has been installed and configured in <b>Ubuntu 16.04</b> OS</p>
<i>For full project posibilities it is suggested more than one pbs_moms.</i>

<h3>Basic project requirements:</h3>
<ul>
  <li><b>Torque pbs</b> - version: 6.0.2</li>
  <li><b>PBS_python</b> library</li>
  <li><b>PAM</b> library</li>
</ul>

<h3>System libraries required</h3>
<ul>
  <li>
    <b>Python software properties</b>
    <ul>
      <li>$ apt-get install python-software-properties</li>
    </ul>
  </li>
  <li>
    <b>Java 8</b>
    <ul>
      <li>$ add-apt-repository ppa:webupd8team/javaapt-get update</li>
      <li>$ apt-get update</li>
      <li>$ apt-get install oracle-java8-installer</li>
    </ul>
  </li>
  <li>
    <b>Torque required libs</b>
    <ul>
      <li>$ apt-get install libxml2-dev</li>
      <li>$ apt-get install libssl-dev</li>
      <li>$ apt-get install tk8.5 tcl8.5</li>
      <li>$ apt-get install gcc</li>
      <li>$ apt-get install g++</li>
      <li>$ apt-get install libtool</li>
      <li>$ apt-get install libboost-all-dev</li>
    </ul>
  </li>
</ul>

<h3>Torque installation and configuration in Ubuntu 16.04</h3>
<ul>
  <li>
    <b>Install</b>
    <ul>
      <li>Download Torque V6.0.2 from <a href="https://www.adaptivecomputing.com">Adaptive computing</a></li>
      <li>Extract files</li>
      <li>$ mv &lt;torque_directory&gt; /usr/local/</li>
      <li>$ cd /usr/local/&lt;torque_directory&gt;</li>
      <li>$ ./configure</li>
      <li>$ make</li>
      <li>$ make install</li>
      <li>$ su</li>
      <li>$ echo /usr/local/lib > /etc/ld.so.conf.d/torque.conf</li>
      <li>$ ldconfig</li>
      <li>$ ./torque.setup root</li>
    </ul>
  </li>
  <li>
    <b>Initialize</b>
    <ul>
      <li>$ pbs_server trqauthd pbs_mom pbs_sched</li>
    </ul>
  </li>
  <li>
    <b>Configure</b>
    <ul>
      <li>$ qmgr -c "p s"</li>
      <li>$ qmgr -c 'set server submit_hosts = localhost'</li>
      <li>$ qmgr -c 'set server allow_node_submit = True'</li>
      <li>$ qmgr -c "create node &lt;hostname%gt;"</li>
    </ul>
  </li>
</ul>

<h3>PBS_python installation and configuration in Ubuntu 16.04</h3>
<ul>
  <li>
    <b>Install</b>
    <ul>
      <li>Download PBS_python from <a href="https://oss.trac.surfsara.nl/pbs_python/wiki/TorqueInstallation">Surfsara</a></li>
      <li>Extract files</li>
      <li>$ mv &lt;pbs_python_directory&gt; /usr/local/</li>
      <li>$ cd /usr/include</li>
      <li>$ mkdir torque</li>
      <li>$ cp /usr/local/&lt;pbs_python_directory&gt;/src/C++/log.h /usr/include/torque</li>
      <li>$ cd /usr/local/&lt;pbs_python_directory&gt;</li>
      <li>$ ./configure</li>
      <li>$ make</li>
      <li>$ make install</li>
    </ul>
  </li>
  <li>
    <b>Import pbs from every directory</b>
    <p>Copy all files <b>from</b>: /usr/local/lib/python2.7/site-packages/pbs/
    <b>to</b>: /usr/local/lib/python2.7/dist-packages/</p>
  </li>
</ul>

