# TORQUE-PBS-APP
<h3>Restful web application, allows users to interact with Torque pbs over a WEB UI</h3>
<p>e.g. Submit, manage jobs and monitor cluster resources</p>

<p>The project has been installed and configured in <b>Ubuntu 16.04</b> OS</p>

<i>For full project posibilities it is suggested more than one pbs_moms.</i>

Basic project requirements:
<ul>
  <li><b>Torque pbs</b> - version: 6.0.2 - available at: <a href="https://www.adaptivecomputing.com">Adaptive computing</a></li>
  <li><b>Pbs_python</b> library - available at <a href="https://oss.trac.surfsara.nl/pbs_python/">Surfsara</a></li>
</ul>

<h4>System libraries required</h4>
<ul>
  <li>
    <b>Python software properties</b>
    <ul>
      <li>$ apt-get install python-software-properties</li>
    </ul>
  </li>
  <li>
    <b>Java 8 install</b>
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

<h4>Torque install and configuration in Ubuntu 16.04</h4>
