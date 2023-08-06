#! /usr/bin/env python
# -*- coding: utf-8 -*-

import hot, es, dataDispose, itemCF, test, time
#import es, test

def startUpdateHot(isTest):
	es.setEnv(isTest)
	hot.startUpdate(isTest, 'config.ini')

def disposeData(isTest):
	es.setEnv(isTest)
	dataDispose.cycleDisposePersonas()

def cfItem(isTest):
	es.setEnv(isTest)
	itemCF.cf()

def updateHistoryActions(isTest):
	es.setEnv(isTest)
	dataDispose.updateHistoryActions()

def logToHive(isTest):
	es.setEnv(isTest)
	test.logToHive()

def testFunc(isTest):
	#disposeData(isTest)
	es.setEnv(isTest)
	#hot.startUpdate(isTest, 'config.ini')
	#print(es.searchDbConfig())
	#print('delete post works record: ' + ('success ' if dataDispose.deletePastWorksRecord() else 'fail '))
	#dataDispose.deletePastWorksRecord()
	test.test()
	'''
	while True:
		es.setEnv(isTest)
		#es.updateRedisWorksHots({'f7106cef64660d0e148d98d77290ff92': 85295.45051608284})
		print(es.searchDbConfig())
		time.sleep(2)
	'''
	
