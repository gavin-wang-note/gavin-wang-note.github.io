---
layout:     post
title:      "Jenkins Email Template"
subtitle:   "Jenkins of Email template"
date:       2023-05-12
author:     "Gavin"
catalog:    true
tags:
    - Jenkins 
    - Automation
---


# Overview

Recently in organizing the documentation, I remembered that some time ago, I redid the jenkins environment, using the latest version, and the email template was adjusted a bit, so here is a record of the recent template used in the current CI environment (Jenkins).

# Script of email teplate

```
<STYLE>
  BODY, TABLE, TD, TH, P {
    font-family: Calibri, Verdana, Helvetica, sans serif;
    font-size: 12px;
    color: black;
  }
  .console {
    font-family: Courier New;
  }
  .filesChanged {
    width: 10%;
    padding-left: 10px;
  }
  .section {
    width: 100%;
    border: thin black dotted;
  }
  .td-title-main {
    color: white;
    font-size: 200%;
    padding-left: 5px;
    font-weight: bold;
  }
  .td-title {
    color: white;
    font-size: 120%;
    font-weight: bold;
    padding-left: 5px;
    text-transform: uppercase;
  }
  .td-title-tests {
    font-weight: bold;
    font-size: 120%;
  }
  .td-header-maven-module {
    font-weight: bold;
    font-size: 120%;    
  }
  .td-maven-artifact {
    padding-left: 5px;
  }
  .tr-title {
    background-color: <%= (build.result == null || build.result.toString() == 'SUCCESS') ? '#27AE60' : build.result.toString() == 'FAILURE' ? '#E74C3C' : '#f4e242' %>;
  }
  .test {
    padding-left: 20px;
  }
  .test-fixed {
  	font-weight: bold;
    font-size: 120%;
    color: #27AE60;
  }
  .test-failed {
  	font-weight: bold;
    font-size: 120%;
    color: #FF0000;
  }
  .test-passed {
  	font-weight: bold;
    font-size: 120%;
    color: #008000;
  }
  .test-skiped {
  	font-weight: bold;
    font-size: 120%;
    color: #3366ff;
  }
  .test-broken {
   	font-weight: bold;
    font-size: 120%;
    color: #800000;
  }
</STYLE>
<BODY>
  <!-- BUILD RESULT -->
  	<%
        def envOverrides = it.getAction("org.jenkinsci.plugins.workflow.cps.EnvActionImpl").getOverriddenEnvironment()
        product_version = envOverrides["PRODUCT_VERSION"]
    %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title-main" colspan=2>
        BUILD ${build.result ?: 'COMPLETED'}
      </td>
    </tr>
    <tr>
      <td>URL:</td>
      <td><A href="${rooturl}${build.url}">${rooturl}${build.url}</A></td>
    </tr>
    <tr>
      <td>Project:</td>
      <td>${project.name}</td>
    </tr>
    <tr>
    <tr>
      <td>Product Version:</td>
      <td>${product_version}</td>
    </tr>
    <tr>
      <td>Date:</td>
      <td>${it.timestampString}</td>
    </tr>
    <tr>
      <td>Duration:</td>
      <td>${build.durationString}</td>
    </tr>
    <tr>
      <td>Cause:</td>
      <td><% build.causes.each() { cause -> %> ${hudson.Util.xmlEscape(cause.shortDescription)} <%  } %></td>
    </tr>
  </table>
  <br/>

  <!-- CHANGE SET -->
  <%
  def changeSets = build.changeSets
  if(changeSets != null) {
    def hadChanges = false %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">CHANGES</td>
    </tr>
    <% changeSets.each() { 
      cs_list -> cs_list.each() { 
        cs -> hadChanges = true %>
    <tr>
      <td>
        Revision
        <%= cs.metaClass.hasProperty('commitId') ? cs.commitId : cs.metaClass.hasProperty('revision') ? cs.revision : cs.metaClass.hasProperty('changeNumber') ? cs.changeNumber : "" %>
        by <B><%= cs.author %></B>
      </td>
      <td>${cs.msgAnnotated}</td>
    </tr>
        <% cs.affectedFiles.each() {
          p -> %>
    <tr>
      <td class="filesChanged">${p.editType.name}</td>
      <td>${p.path}</td>
    </tr>
        <% }
      }
    }
    if ( !hadChanges ) { %>
    <tr>
      <td colspan="2">No Changes</td>
    </tr>
    <% } %>
  </table>
  <br/>
  <% } %>

<!-- ARTIFACTS -->
  <% 
  def artifacts = build.artifacts
  if ( artifacts != null && artifacts.size() > 0 ) { %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title">BUILD ARTIFACTS</td>
    </tr>
    <% artifacts.each() {
      f -> %>
      <tr>
        <td>
          <a href="${rooturl}${build.url}artifact/${f}">${f}</a>
      </td>
    </tr>
    <% } %>
  </table>
  <br/>
  <% } %>

<!-- MAVEN ARTIFACTS -->
  <%
  try {
    def mbuilds = build.moduleBuilds
    if ( mbuilds != null ) { %>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title">BUILD ARTIFACTS</td>
    </tr>
      <%
      try {
        mbuilds.each() {
          m -> %>
    <tr>
      <td class="td-header-maven-module">${m.key.displayName}</td>
    </tr>
          <%
          m.value.each() { 
            mvnbld -> def artifactz = mvnbld.artifacts
            if ( artifactz != null && artifactz.size() > 0) { %>
    <tr>
      <td class="td-maven-artifact">
              <% artifactz.each() {
                f -> %>
        <a href="${rooturl}${mvnbld.url}artifact/${f}">${f}</a><br/>
              <% } %>
      </td>
    </tr>
            <% }
          }
        }
      } catch(e) {
        // we don't do anything
      } %>
  </table>
  <br/>
    <% }
  } catch(e) {
    // we don't do anything
  } %>

<!-- Allure Result -->
<%
  lastAllureReportBuildAction = build.getAction(ru.yandex.qatools.allure.jenkins.AllureReportBuildAction.class)
  if (lastAllureReportBuildAction) {
    allureResultsUrl = "${rooturl}${build.url}allure"
    allureLastBuildSuccessRate = String.format("%.2f", lastAllureReportBuildAction.getPassedCount() * 100f / lastAllureReportBuildAction.getTotalCount())
  }
%>

<%
pylintResultsUrl = "${build.environment['JOB_URL']}warnings50/trendGraph"
coberturaResultsUrl = "${rooturl}${build.url}cobertura"
%>

<%
   def total = lastAllureReportBuildAction.getPassedCount() + lastAllureReportBuildAction.getFailedCount() + lastAllureReportBuildAction.getSkipCount() + lastAllureReportBuildAction.getBrokenCount()
%>

  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="7">Test Cases Status</td>
    </tr>
    <tr>
        <td class="td-title-tests">Name</td>
        <td class="test-fixed">Total</td>
        <td class="test-passed">Passed</td>
        <td class="td-title-tests">Success Rate</td>
        <td class="test-failed">Failed</td>
        <td class="test-skiped">Skipped</td>
        <td class="test-broken">Broken</td>
      </tr>
    <tr>    	
      <td>${project.name}</td>
      <td class="test-fixed">${total}</td>
      <td class="test-passed">${lastAllureReportBuildAction.getPassedCount()}</td>
      <td  class="test-fixed">${allureLastBuildSuccessRate}% </td>
      <td class="test-failed">${lastAllureReportBuildAction.getFailedCount()}</td>
      <td class="test-skiped">${lastAllureReportBuildAction.getSkipCount()}</td>
      <td  class="test-broken">${lastAllureReportBuildAction.getBrokenCount()}</td>
    </tr>
  </table>

<br> </br>

<!-- CI of Allure/Pyline/Cobertura -->
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">Allure history trend</td>
    </tr>
  </table>

  <table>
    <tr>
       <img lazymap="${allureResultsUrl}/graphMap" src="${allureResultsUrl}/graph" width="500px" height="200px"/>
    </tr>
  </table>

<br> </br>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">PyLint Warnings Trend</td>
    </tr>
  </table>

  <table>
    <tr>
        <img src="EMAIL_BASE64_IMG_REPLACE" width="500px" height="200px"/>
    </tr>
  </table>

<br> </br>
  <table class="section">
    <tr class="tr-title">
      <td class="td-title" colspan="2">Code Coverage</td>
    </tr>
  </table>

  <table>
    <tr>
        <img lazymap="${coberturaResultsUrl}/graphMap" src="${coberturaResultsUrl}/graph" width="500px" height="200px"/> 
   </tr>
  </table>

<!-- CONSOLE OUTPUT -->
  <%
  if ( build.result == hudson.model.Result.FAILURE ) { %>
  <table class="section" cellpadding="0" cellspacing="0">
    <tr class="tr-title">
      <td class="td-title">CONSOLE OUTPUT</td>
    </tr>
    <% 	build.getLog(100).each() {
      line -> %>
	  <tr>
      <td class="console">${org.apache.commons.lang.StringEscapeUtils.escapeHtml(line)}</td>
    </tr>
    <% } %>
  </table>
  <br/>
  <% } %>
</BODY>
```

Description:

This file, placed in the email-templates directory in the Jenkins installation directory (if this directory does not exist, just create it manually, and note this directory's ownership information), for example: ${JENKINS_INSTALL_PATH}/email-templates/v1.1_allure-pipeline- report.groovy


# Cell phone terminal display effect picture:

<img class="shadow" src="/img/in-post/cell_phone_of_jenkins_email.jpg" width="1200">

