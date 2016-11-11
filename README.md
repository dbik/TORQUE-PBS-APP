# TORQUE-PBS-APP
<h1>Under construction -- <i>Updating back end, replace AngularJS instead of ExtJS</i></h1>
<h3>Restful web application that allows users to interact with Torque pbs through a WEB UI</h3>
<p>Submit, manage jobs and monitor cluster resources</p>

<h3>Basic project requirements:</h3>
<ul>
  <li><b>UBUNTU</b> - version: 16.04</li>
  <li><b>PYTHON</b> - version: 2.7</li>
  <li><b>TORQUE PBS</b> - version: 6.0.2</li>
</ul>
<p>I assume you already have latest versions of <b>PIP, VIRTUAL-ENV, VIRTUAL-ENV-WRAPPER</b> installed and configured.</p>
<ul>
  <li>
    <h3>System libraries required</h3>
      <ul>
        <li>
          <b>Python software properties</b>
          <ul>
            <li>$ apt-get install python-software-properties</li>
          </ul>
        </li>
        <li>
          <b>Python &amp; MySQL</b>
          <ul>
            <li>apt install mysql-server mysql-client</li>
            <li>$ mysql_secure_installation</li>
            <li>$ apt-get install libmysqlclient-dev</li>
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
    </li>
    <li>
      <h3>Torque installation and configuration in Ubuntu 16.04</h3>
      <ul>
        <li>
          <b>Install</b>
          <ul>
            <li>Download Torque V6.0.2 from <a href="https://www.adaptivecomputing.com/downloading/?file=/torque/torque-6.0.2-1469811694_d9a3483.tar.gz">Adaptive computing</a></li>
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
            <li>$ qmgr -c "create node &lt;hostname&gt;"</li>
          </ul>
        </li>
      </ul>
    </li>
</ul>

<i>For full project posibilities it is suggested more than one pbs_moms.</i>
