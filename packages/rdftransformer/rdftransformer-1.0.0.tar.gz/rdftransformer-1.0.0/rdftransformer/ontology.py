# -*- coding: utf-8 -*-

import re
import os.path
import json
import rdflib
import ast
from helpers import printp, dict_merge
from evaluator import *

class Ontology:

	# constructor of the Ontology class
	# ATTENTION! Ontology should be in turtle-format
	def __init__(self, ontologyLocation, annotationPrefix):
		self.ontologyLocation = ontologyLocation
		if self.__validateOntologyLocation():

			# imports and defining output prefix
			self.ontology_raw = self.__importOntologyRaw()
			self.ontology = self.__importOntology()
			self.annotationPrefix = annotationPrefix
			self.fileNamespace = None

			# gather information:
			# 	- prefixes
			# 	- classes with - for now - property restrictions
			#	- object properties
			# 	- data properties
			self.ontologyPrefixes = self.__getOntologyPrefixes()
			self.classes = self.__getClasses()
			self.objectProperties = self.__getObjectProperties()
			self.dataProperties = self.__getDataProperties()
			self.errors = []
			
		else:
			print("File not Found!")


	# checks if the ontology exists in the given directory
	def __validateOntologyLocation(self):
		return os.path.isfile(self.ontologyLocation)


	# imports the ontology in plain text
	def __importOntologyRaw(self):
		fd = open(self.ontologyLocation, "r")
		read_data = []
		for line in fd:
			read_data.append(line)
		fd.close()
		return read_data


	# imports ontology and compresses whole json-ld
	# structure into a dict with all necessary
	# information for further easier processing
	def __importOntology(self):
		g=rdflib.Graph()
		g.load(self.ontologyLocation, format='turtle')
		j =  g.serialize(format = "json-ld")
		j = ast.literal_eval(j)
		return evaluateOntology(j) # see evaluator.py


	# extracting and saving all the prefixes
	# in the ontology as a dict
	def __getOntologyPrefixes(self):
		prefixes = {}

		for line in self.ontology_raw:
			if '@prefix' in line:
				line = ''.join(line.split())
				prefix = line[7: line.find(":")]
				source = line[line.find("<")+1 : line.find(">")]
				prefixes[prefix] = source

		return prefixes


	# returns the substitute of a prefix
	# example: "https://w3id.org/alkis/" would return "alkis" or None
	def __getPrefixSubstitute(self, prefix):
		for key in self.ontologyPrefixes:
			if prefix in self.ontologyPrefixes[key]:
				return key


	# https://w3id.org/alkis/angabenZumAbschnittStelle returns
	# {
	# 	"prefix" : "https://w3id.org/alkis/",
	# 	"prefix_substitute" : "alkis" or None,
	# 	"name" : "angabenZumAbschnittStelle"
	# }
	def __getClassInfos(self, full_class):
		delimiters = ["/", "#"]
		for delimiter in delimiters:
			classPrefix = full_class[:full_class.rfind(delimiter)+1]
			classPrefixSubstitute = self.__getPrefixSubstitute(classPrefix)
			className = full_class[full_class.rfind(delimiter)+1:]
			if (delimiters[0] not in className) and (delimiters[1] not in className):
				class_infos = {}
				class_infos["prefix"] = classPrefix
				class_infos["prefix_substitute"] = classPrefixSubstitute
				class_infos["name"] = className
				return class_infos


	# if a restriction has a min and a max cardinality constraint,
	# combine the two into one
	# example:
	# anteil has minQualifiedCardinality 2, resulting in the array ["2", "*"]
	# anteil has also maxQualifiedCardinality 4, resulting in the array ["*", "4"]
	# after editing the output array looks like this ["2", "4"]
	def __editCardinalities(self, cardinality_old, cardinality_new):
		cardinality = []

		if ("*" in cardinality_old[0]) and ("*" not in cardinality_new[0]):
			cardinality.append(cardinality_new[0])
		else:
			cardinality.append(cardinality_old[0])


		if ("*" in cardinality_old[1]) and ("*" not in cardinality_new[1]):
			cardinality.append(cardinality_new[1])
		else:
			cardinality.append(cardinality_old[1])

		return cardinality


	# checks and changes cardinality values if a property has both
	# maxQualifiedCardinality and minQualifiedCardinality for the same range classes or datatypes
	# returns a restriction dict
	def __checkCardinalities(self, old, new):
		property_name = new.keys()[0]
		if old and (property_name in old.keys()):
			if ("onClass" in old[property_name].keys()) and ("onClass" in new[property_name].keys()):
				if old[property_name]["onClass"] == new[property_name]["onClass"]:
					cardinality_old = old[property_name]["cardinality"]
					cardinality_new = new[property_name]["cardinality"]
					new[property_name]["cardinality"] = self.__editCardinalities(cardinality_old, cardinality_new)

			if ("onDataRange" in old[property_name].keys()) and ("onDataRange" in new[property_name].keys()):
				if old[property_name]["onDataRange"] == new[property_name]["onDataRange"]:
					cardinality_old = old[property_name]["cardinality"]
					cardinality_new = new[property_name]["cardinality"]
					new[property_name]["cardinality"] = self.__editCardinalities(cardinality_old, cardinality_new)

		return new


	# checks if a restriction has the range of a class or datatype like xsd:string
	# returns either
	# "onClass": {
	#   "LinearRing": "ngeo"
	# }
	# or 
	# "onDataRange": {
	#   "dateTime": "xsd"
	# }
	def __getOnDataOrClass(self, restriction_class):
		if "http://www.w3.org/2002/07/owl#onClass" in restriction_class.keys():
			onClass = {}
			class_info = self.__getClassInfos(restriction_class["http://www.w3.org/2002/07/owl#onClass"][0])
			onClass.update({ "onClass" : {class_info["name"] : class_info["prefix_substitute"]}})
			return onClass

		elif "http://www.w3.org/2002/07/owl#onDataRange" in restriction_class.keys():
			onDataRange = {}
			class_info = self.__getClassInfos(restriction_class["http://www.w3.org/2002/07/owl#onDataRange"][0])
			onDataRange.update({ "onDataRange" : {class_info["name"] : class_info["prefix_substitute"]}})
			return onDataRange

		else:
			return None


	# extracts the cardinality infos for a restriction
	def __getCardinalityInfos(self, restriction_class, cardinality_name):
		cardinality = {}
		restriction_value = restriction_class[cardinality_name]["value"]

		restriction_range = []

		if "http://www.w3.org/2002/07/owl#minQualifiedCardinality" in cardinality_name:
			restriction_range.append(restriction_value)
			restriction_range.append("*")

		if "http://www.w3.org/2002/07/owl#maxQualifiedCardinality" in cardinality_name:
			restriction_range.append("*")
			restriction_range.append(restriction_value)

		if ("http://www.w3.org/2002/07/owl#qualifiedCardinality" in cardinality_name) or ("http://www.w3.org/2002/07/owl#cardinality" in cardinality_name):
			restriction_range.append(restriction_value)
			restriction_range.append(restriction_value)

		cardinality.update({"cardinality" : restriction_range})

		if ("http://www.w3.org/2002/07/owl#cardinality" not in cardinality_name):
			cardinality.update(self.__getOnDataOrClass(restriction_class))

		return cardinality


	# looks if a restrictions has allValuesFrom or someValuesFrom as cardinality and returns them
	def __getAllOrSomeValues(self, restriction_class, someOrAll):
		cardinality = {}

		restriction_range = []

		if "http://www.w3.org/2002/07/owl#someValuesFrom" in someOrAll:
			restriction_range.append("1")
			restriction_range.append("*")

		if "http://www.w3.org/2002/07/owl#allValuesFrom" in someOrAll:
			restriction_range.append("*")
			restriction_range.append("*")

		class_infos = self.__getClassInfos(restriction_class[someOrAll][0])

		cardinality.update({"cardinality" : restriction_range})
		cardinality.update({"onClass" : {class_infos["name"] : class_infos["prefix_substitute"]}})


		return cardinality


	# gets the cardinality for a given restriction and checks if its a
	# cardinality constraint or values constraint
	def __getCardinalities(self, restriction_class):
		for key in restriction_class.keys():
			if ("Cardinality" in key) or ("cardinality" in key):
				return  self.__getCardinalityInfos(restriction_class, key)
			if ("someValuesFrom" in key) or ("allValuesFrom" in key):
				return self.__getAllOrSomeValues(restriction_class, key)
		return None


	# returns a dict with all restrictions for a class, including superclasses
	def __getAllRestrictionsForClass(self, class_name):
		class_restrictions = self.__getRestrictionsForClass(class_name)
		superclass_restrictions = self.__getSuperclassRestrictions(class_name)
		restrictions = dict_merge(class_restrictions, superclass_restrictions)
		if restrictions:
			return {"onProperty" : restrictions}
		

	# returns a dict with all restrictions for a class
 	def __getRestrictionsForClass(self, class_name):
 		if "http://www.w3.org/2000/01/rdf-schema#subClassOf" in self.ontology[class_name].keys():
 			superclasses = self.ontology[class_name]["http://www.w3.org/2000/01/rdf-schema#subClassOf"]
 			restrictions = {}
 			for superclass in superclasses:
 				if isinstance(superclass, dict):
 					if "http://www.w3.org/2002/07/owl#Restriction" in superclass["rdf:type"]:
 						restriction = self.__checkCardinalities(restrictions, self.__getRestriction(superclass))
 						restrictions.update(restriction)
 			return restrictions


 	# returns a dict with all restrictions of all superclasses for one class
 	def __getSuperclassRestrictions(self, class_name, superclasses = {}):
 		if "http://www.w3.org/2000/01/rdf-schema#subClassOf" in self.ontology[class_name].keys():
 			subClassOf = self.ontology[class_name]["http://www.w3.org/2000/01/rdf-schema#subClassOf"]
 			for element in subClassOf:
 				if isinstance(element, str):
 					# print "\t\t\tSTRING ---- " + element
 					superclasses = dict_merge(superclasses, self.__getSuperclassRestrictions(element, self.__getRestrictionsForClass(element)))

 				# NOT USED YET
 				# if isinstance(element, dict):
 				# 	return
 				# 	# print "\tDICT"
 				# 	if "http://www.w3.org/2002/07/owl#Class" in element["rdf:type"]:

 				# 		if "http://www.w3.org/2002/07/owl#complementOf" in element.keys():
 				# 			# print "----COMPLEMENTOF"
 				# 			return

 				# 		if "http://www.w3.org/2002/07/owl#intersectionOf" in element.keys():
 				# 			# print "----INTERSECTION"
 				# 			return

 				# 		if "http://www.w3.org/2002/07/owl#unionOf" in element.keys():
 				# 			# print "----UNION"
 				# 			return

 		return superclasses


	# returns a dict with all necessary information on a restriction
	def __getRestriction(self, subclass):
		restriction = {}
		property_dict = {} 
		subclass_name = subclass["http://www.w3.org/2002/07/owl#onProperty"][0]
		class_infos =  self.__getClassInfos(subclass_name)
		property_prefix = class_infos["prefix_substitute"]
		property_name = class_infos["name"]
		property_cardinalities = self.__getCardinalities(subclass)
		property_dict.update({"prefix" : property_prefix})
		if property_cardinalities:
			property_dict.update(property_cardinalities)
		restriction.update({property_name : property_dict})
		return restriction
	

	# saves classes in a dictionary
	# ordered by the prefix substitutes
	def __getClasses(self):
		classes = {}
		for key in self.ontology.keys():
			if "#Class" in self.ontology[key]["rdf:type"]:
				class_infos = self.__getClassInfos(key)
				classes.setdefault(class_infos["prefix_substitute"],{}).update({class_infos["name"] : {}})
				restrictions = self.__getAllRestrictionsForClass(key)
				if restrictions:
					classes.setdefault(class_infos["prefix_substitute"],{}).update({class_infos["name"] : {"restrictions" : restrictions}})

		return classes


	# checks for subclasses in an object property
	def __getSubClasses(self, className):
		subClasses = []
		for nodeName in self.ontology:
			node = self.ontology[nodeName]
			if "http://www.w3.org/2002/07/owl#Class" in node["rdf:type"]:
				if "http://www.w3.org/2000/01/rdf-schema#subClassOf" in node.keys():
					superClasses = node["http://www.w3.org/2000/01/rdf-schema#subClassOf"]
					for superClass in superClasses:
						if isinstance(superClass, dict):
							if "http://www.w3.org/2002/07/owl#Class" in superClass["rdf:type"]:
								for names in superClass.values():
									if isinstance(names, list):
										for name in names:
											if className == name:
												subClasses.append(nodeName)
						if isinstance(superClass, str):
							if superClass == className:
								subClasses.append(nodeName)
		return subClasses


	# gets the classes in the domain of a property and returns
	# a dict in the form of { name : prefix }
	# example:
	# {
	# 	"AX_Flurstueck": "alkis", 
	# 	"AX_Flurstueck_Kerndaten": "alkis"
	# }
	def __getDomainForProperty(self, key):
		domainClasses = {}
		if "http://www.w3.org/2000/01/rdf-schema#domain" in self.ontology[key]:
			for domain in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#domain"]:
				class_infos = self.__getClassInfos(domain)
				domainClasses.update({class_infos["name"]: class_infos["prefix_substitute"]})
				for subClass in self.__getSubClasses(domain):
					subclass_infos = self.__getClassInfos(subClass)
					domainClasses.update({subclass_infos["name"] : subclass_infos["prefix_substitute"]})
		return domainClasses


	# gets the classes in the range of a property and returns
	# a dict in the form of { name : prefix }
	# example:
	# {
	# 	"AX_Flurstueck": "alkis", 
	# 	"AX_Flurstueck_Kerndaten": "alkis"
	# }
	def __getRangeForProperty(self, key):
		rangeClasses = {}
		if "http://www.w3.org/2000/01/rdf-schema#range" in self.ontology[key]:
			for rangeName in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#range"]:
				class_infos = self.__getClassInfos(rangeName)
				rangeClasses.update({class_infos["name"]: class_infos["prefix_substitute"]})
				for subClass in self.__getSubClasses(rangeName):
					subclass_infos = self.__getClassInfos(subClass)
					rangeClasses.update({subclass_infos["name"] : subclass_infos["prefix_substitute"]})
		return rangeClasses


	# saves object properties in a dictionary
	# ordered by the prefix substitutes
	def __getObjectProperties(self):
		objectProperties = {}
		for key in self.ontology.keys():
			if "#ObjectProperty" in self.ontology[key]["rdf:type"]:
				class_infos = self.__getClassInfos(key)
				
				domainClasses = self.__getDomainForProperty(key)

				rangeClasses = self.__getRangeForProperty(key)

				domainDict = {"domain" : domainClasses}
				rangeDict = {"range" : rangeClasses}
				prop = {}
				prop.setdefault(class_infos["name"],{}).update(domainDict)
				prop.setdefault(class_infos["name"],{}).update(rangeDict)

				objectProperties.setdefault(class_infos["prefix_substitute"], {}).update(prop)
		return objectProperties


	# saves datatype properties in a dictionary
	# ordered by the prefix substitutes
	def __getDataProperties(self):
		dataProperties = {}
		for key in self.ontology.keys():
			if "#DatatypeProperty" in self.ontology[key]["rdf:type"]:
				class_infos = self.__getClassInfos(key)
				
				domainClasses = self.__getDomainForProperty(key)

				rangeClasses = self.__getRangeForProperty(key)

				domainDict = {"domain" : domainClasses}
				rangeDict = {"range" : rangeClasses}
				prop = {}
				prop.setdefault(class_infos["name"],{}).update(domainDict)
				prop.setdefault(class_infos["name"],{}).update(rangeDict)

				dataProperties.setdefault(class_infos["prefix_substitute"], {}).update(prop)
		return dataProperties


	# sets the variable fileNamespace, to connect the base namespace
	# of the imported file and the preferred annotation prefix
	def setFileNamespace(self, baseNamespace):
		self.fileNamespace = { baseNamespace : self.ontologyPrefixes[self.annotationPrefix]}


	# gets the corresponding ontology prefix for file prefix
	def resolveFilePrefix(self, prefix):
		if self.fileNamespace:
			if prefix in self.fileNamespace.keys():
				prefix = self.fileNamespace[prefix]

		return  self.__getPrefixSubstitute(prefix)


	# gets the corresponding file prefix for ontology prefix
	def __resolveOntologyPrefix(self, prefix):
		prefix = None
		if self.fileNamespace:
			for key in self.fileNamespace:
				prefix =  self.fileNamespace[key]
				for p in self.ontologyPrefixes:
					if prefix == self.ontologyPrefixes[p]:
						prefix = key

		return prefix


	# checks if an lxml.etree._Element is a class of the ontology
	def isClass(self, tag_infos):
		tag_name = tag_infos["name"]
		tag_prefix = self.resolveFilePrefix(tag_infos["prefix"])

		if tag_prefix in self.classes.keys():
			if tag_name in self.classes[tag_prefix].keys():
				return True
				
		return False


	def isObjectProperty(self, tag_infos):
		tag_name = tag_infos["name"]
		tag_prefix = self.resolveFilePrefix(tag_infos["prefix"])

		if tag_prefix in self.objectProperties.keys():
			if tag_name in self.objectProperties[tag_prefix].keys():
				return True

		return False


	def isDataTypeProperty(self, tag_infos):
		tag_name = tag_infos["name"]
		tag_prefix = self.resolveFilePrefix(tag_infos["prefix"])

		if tag_prefix in self.dataProperties.keys():
			if tag_name in self.dataProperties[tag_prefix].keys():
				return True

		return False


	def __getPropertyOfData(self, properties, name, prefix):
		for prop in properties:
			if (prop["prefix"] == prefix) and (prop["name"] == name):
				return prop
		return None


	def __getFrequencyOfPropertyOfData(self, properties, name, prefix):
		for prop in properties:
			if (prop["prefix"] == prefix) and (prop["name"] == name):
				return prop["frequency"]
		return None

	def verifyCardinalities(self, properties, current_element):
		restrictions = {}
		element_name = current_element["name"]
		# print element_name
		element_prefix = self.resolveFilePrefix(current_element["prefix"])
		if element_prefix in self.classes.keys():
			if element_name in self.classes[element_prefix].keys():
				restrictions = self.classes[element_prefix][element_name]
		# restrictions = self.classes[tag_prefix][tag_name]

		if restrictions:
			for property_name in restrictions["restrictions"]["onProperty"]:
				restriction = restrictions["restrictions"]["onProperty"][property_name]
				prefix = self.__resolveOntologyPrefix(restriction["prefix"])
				cardinality = restriction["cardinality"]
				property_all = self.__getPropertyOfData(properties, property_name, prefix)
				if property_all:
					frequency = property_all["frequency"]
					if (cardinality[0] == "*"):
						# print "\tmax " + str(cardinality[1])
						if frequency > int(cardinality[1]):
							property_all["valid"] = False
							self.errors.append("[Error] Property Error: '" + property_name + "' is allwoed to occur at max " + cardinality[1] +  " times in data file, but occurs " + str(frequency) + " times")

					if (cardinality[1] == "*"):
						# print "\tmin " + str(cardinality[1])
						if frequency < int(cardinality[1]):
							property_all["valid"] = False
							self.errors.append("[Error] Property Error: '" + property_name + "' has to occur at least " + cardinality[0] +  " times in data file, but occurs " + str(frequency) + " times")


					if (cardinality[0].isdigit()) and (cardinality[1].isdigit()):
						if cardinality[0] == cardinality[1]:
							# print "\texactly "  + str(cardinality[0])
							if frequency != int(cardinality[0]):
								property_all["valid"] = False
								self.errors.append("[Error] Property Error: '" + property_name + "' has to occur " + cardinality[0] +  " times in data file, but occurs " + str(frequency) + " times")

						if (cardinality[1] > cardinality[0]):
							# print "\tcan occur from " + str(cardinality[0]) + " to " + str(cardinality[1]) + " times"
							if (frequency < cardinality[0]) and (frequency > cardinality[1]):
								property_all["valid"] = False
								self.errors.append("[Error] Property Error: '" + property_name + "' is not in range of [" + str(cardinality[0]) + "," + str(cardinality[0]) + "]. Occurs " + str(frequency) + " times")
				else:
					if (cardinality[1] == "*"):
						self.errors.append("[Error] Property Error: '" + property_name + "' has to occur at least " + cardinality[0] +  " times in data file, but can't be found")
					elif (cardinality[0].isdigit()) and (cardinality[1].isdigit()):
						if cardinality[1] > cardinality[0]:
							self.errors.append("[Error] Property Error: '" + property_name + "' has to be occur " + str(cardinality[0]) + " - " + str(cardinality[1]) + " times, but can't be found")
					else:
						self.errors.append("[Notification] Property: '" + property_name + "' could not be found.")
		return properties


	def checkDomain(self, tag_infos, parent_infos, property_type):
		prefix = self.resolveFilePrefix(tag_infos["prefix"])
		name = tag_infos["name"]

		parent_prefix = self.resolveFilePrefix(parent_infos["prefix"])
		parent_name = parent_infos["name"]
		# print parent_name

		if "objectProperty" in property_type:
			if prefix in self.objectProperties.keys():
				if name in self.objectProperties[prefix].keys():
					domains = self.objectProperties[prefix][name]["domain"]
					for domain_name in domains.keys():
						if parent_name == domain_name:
							if parent_prefix == domains[domain_name]:
								return True

		if "dataTypeProperty" in property_type:
			if prefix in self.dataProperties.keys():
				if name in self.dataProperties[prefix].keys():
					domains = self.dataProperties[prefix][name]["domain"]
					for domain_name in domains.keys():
						if parent_name == domain_name:
							if parent_prefix == domains[domain_name]:
								return True

	def checkRange(self, tag_infos, child_infos):
		prefix = self.resolveFilePrefix(tag_infos["prefix"])
		name = tag_infos["name"]

		child_prefix = self.resolveFilePrefix(child_infos["prefix"])
		child_name = child_infos["name"]

		if prefix in self.objectProperties.keys():
			if name in self.objectProperties[prefix].keys():
				ranges = self.objectProperties[prefix][name]["range"]
				for range_name in ranges.keys():
					if child_name == range_name:
						if child_prefix == ranges[range_name]:
							return True