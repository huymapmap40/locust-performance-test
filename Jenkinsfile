#!/usr/bin/env groovy
@Library('sb-common-pipeline') _

pipeline {
  agent {
    kubernetes {
      defaultContainer 'workflow'
      yaml derivePodTemplate(from: 'podTemplates/workflow-slim.yaml',
        sa: 'jenkins-slave-scaling-operator')
    }
  }
  options {
    timeout(time: 1, unit: 'HOURS')
    retry(0)
    quietPeriod(0)
    buildDiscarder(logRotator(numToKeepStr: '30', daysToKeepStr: '90'))
    timestamps()
    ansiColor('xterm')
  }
  parameters {
    booleanParam(
      name: 'DEPLOY_STAGING',
      defaultValue: false,
      description: 'set to true to deploy app')
    string(
      name: 'STAGING_ENVIRONMENTS',
      defaultValue: 'staging-ph staging-id staging-sg staging-tw staging-kr staging-my staging-th',
      description: '''
          space separated list of app.
          this parameter only affects deployment, when DEPLOY_STAGING=true.
      ''')
    string(
      name: 'RELEASE_VERSION',
      defaultValue: '',
      description: '''
        this parameter affects only master branch builds
        if DEPLOY_STAGING=false and RELEASE_VERSION=''        - create new tag by incrementing minor version of previous tag
        if DEPLOY_STAGING=false and RELEASE_VERSION='v1.2.3'  - create new tag 'v1.2.3'

        if DEPLOY_STAGING=true and RELEASE_VERSION=''         - use latest tag to deploy to prod environments
        if DEPLOY_STAGING=true and RELEASE_VERSION='v1.2.3'   - deploy 'v1.2.3' to prod environments (image for v1.2.3 must exist)
      ''')
    booleanParam(
      name: 'DELETE_DEPLOYMENT',
      defaultValue: false,
      description: 'set to true to delete deployed app')
    string(
      name: 'LOCUST_MODULE',
      defaultValue: '',
      description: 'Example salmon-web-shoppingtrip store-service_vn')
  }
  stages {
    stage("Prepare workspace") {
      when {
        branch 'master'
      }
      steps {
        withCredentials([
          file(credentialsId: 'shopback-kubeconfig', variable: 'KUBE_CONFIG')
        ]) {
          // print build parameters
          sh('''#!/bin/bash
            echo "
            GIT_URL:              $GIT_URL
            GIT_BRANCH:           $GIT_BRANCH
            GIT_COMMIT:           $GIT_COMMIT
            LOCUST_MODULE:        $LOCUST_MODULE
            DEPLOY_STAGING:       $DEPLOY_STAGING
            STAGING_ENVIRONMENTS: $STAGING_ENVIRONMENTS"

            mkdir ~/.kube; mv $KUBE_CONFIG ~/.kube/config && chmod u+w ~/.kube/config
          ''')
        }
      }
    }
    stage("Deploy to staging") {
      when {
        branch 'master'
        environment name: 'DEPLOY_STAGING', value: 'true'
        expression { env.LOCUST_MODULE != null }
      }
      steps {
        sh('''#!/bin/bash -e
          echo "##### STAGING ENV ${STAGING_ENVIRONMENTS} DEPLOYMENT #####"
          echo -e "\nenvironments:\n$(echo ${STAGING_ENVIRONMENTS} | tr ' ' '\n')\n"

          for E in ${STAGING_ENVIRONMENTS}; do
            SB_ENV=$(echo $E | sed 's/production-/prod-/g')
            echo "###### DEPLOYING NEW CLUSTER-${SB_ENV} ######"
            echo "###### KUBECTL SWITCH ${SB_ENV} ######"
            if ! kubectl config use-context ${SB_ENV}; then
              echo -e "\\e[33m===== Unable to kubectl config use-context ${SB_ENV}, skipping deploy ${SB_ENV}=====\\e[39m"
              exit 1
            fi
            ### NEW CODE
            TEAMFOLDER=`grep tasksRoot environments/test_${LOCUST_MODULE}.yaml|awk -F 'tasksRoot: ' '{print $2}'|awk -F 'tasks/' '{print $2}'|sed -e "s/'$//" -e 's/"$//'`
            mkdir -p "tasks/$TEAMFOLDER"
            cp -r tasksall/$TEAMFOLDER tasks
            ###

            echo "###### HELM TEMPLATE ######"
            HELM_TEMP_FILE=helm_$(date +%Y%m%d%H%M%S).yaml
            helm template locust-${LOCUST_MODULE} .\
              -f values.yaml \
              -f environments/test_${LOCUST_MODULE}.yaml \
              --set jenkins=true \
              > ${HELM_TEMP_FILE}
            cat ${HELM_TEMP_FILE}
            echo "###### KUBECTL APPLY ######"
            kubectl create -f ${HELM_TEMP_FILE}
            echo "###### KUBECTL GET ######"
            sleep 5
            kubectl get -f ${HELM_TEMP_FILE}
            echo -e "\n\\e[32m===== deploy to ${SB_ENV} finished =====\\e[39m"
            rm -f ${HELM_TEMP_FILE}
          done
          rm -f kubeconfig
        ''')
      }
    }

    stage("Delete Deployment") {
      when {
        branch 'master'
        environment name: 'DELETE_DEPLOYMENT', value: 'true'
        expression { env.LOCUST_MODULE != null }
      }
      steps {
        sh('''#!/bin/bash -e
          echo "##### STAGING ENV ${STAGING_ENVIRONMENTS} DEPLOYMENT #####"
          echo -e "\nenvironments:\n$(echo ${STAGING_ENVIRONMENTS} | tr ' ' '\n')\n"

          for E in ${STAGING_ENVIRONMENTS}; do
            SB_ENV=$(echo $E | sed 's/production-/prod-/g')
            echo "###### DEPLOYING NEW CLUSTER-${SB_ENV} ######"
            echo "###### KUBECTL SWITCH ${SB_ENV} ######"
            if ! kubectl config use-context ${SB_ENV}; then
              echo -e "\\e[33m===== Unable to kubectl config use-context ${SB_ENV}, skipping deploy ${SB_ENV}=====\\e[39m"
              exit 1
            fi
            echo "###### HELM TEMPLATE ######"
            HELM_TEMP_FILE=helm_$(date +%Y%m%d%H%M%S).yaml
            helm template locust-${LOCUST_MODULE} .\
              -f values.yaml \
              -f environments/test_${LOCUST_MODULE}.yaml \
              --set jenkins=true \
              > ${HELM_TEMP_FILE}
            cat ${HELM_TEMP_FILE}
            echo "###### KUBECTL DELETE APP ######"
            kubectl delete -f ${HELM_TEMP_FILE}
            echo -e "\n\\e[32m===== delete app from ${SB_ENV} finished =====\\e[39m"
            rm -f ${HELM_TEMP_FILE}
          done
          rm -f kubeconfig
        ''')
      }
    }
  }
  post {
    success {
      cleanWs()
    }
  }
}
