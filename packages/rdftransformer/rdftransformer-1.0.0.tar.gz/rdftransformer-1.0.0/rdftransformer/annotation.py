# -*- coding: utf-8 -*-

import re
import os.path
import json
import string, random
from helpers import isDate
from helpers import printp
from ontology import Ontology
from coordinates import UTM
from lxml import etree as ET
from rdflib import Graph, Namespace, Literal, URIRef, BNode, collection
from rdflib import RDF, RDFS, OWL, XSD
from datetime import datetime


class Annotation:

	def __init__(self):
		self.graph = Graph()
		self.indent = 0
		self.depth = 0
		self.errors = []


	def importOntology(self, ontologyLocation, annotationPrefix):
		self.ontology = Ontology(ontologyLocation, annotationPrefix)
		self.ontologyNamespaces = self.__getNamespacesFromOntology()
		self.__addNamespacesToGraph()
		return self.ontology


	def importData(self, filename):
		if self.__validateDataLocation(filename):
			self.data = ET.parse(filename)
			self.root = self.data.getroot()
			self.namespaces = self.root.nsmap
			self.baseNamespace = self.root.tag[self.root.tag.find("{")+1:self.root.tag.find("}")]
			self.ontology.setFileNamespace(self.baseNamespace)
			self.prefix = self.__getDataPrefix()
		else:
			print ("File not found!")
		return self.data


	def getElementsByTagName(self, tag, parent = "", namespaces = {}):
		tag_infos = self.__getTagInfos(tag, ":")
		tagPrefix = tag_infos["prefix"]
		tagName =  tag_infos["name"]

		tag_infos_parent = self.__getTagInfos(parent, ":")
		parentPrefix = tag_infos_parent["prefix"]
		parentName = tag_infos_parent["name"]

		if not namespaces:
			if tagPrefix in self.namespaces:
				tagQuery =  "{" + self.namespaces[tagPrefix] + "}" + tagName
			else:
				tagQuery = tagName

			if parentPrefix in self.namespaces:
				parentQuery = "{" + self.namespaces[parentPrefix] + "}" + parentName
			else:
				parentQuery = parentName
		else:
			if tagPrefix in namespaces.keys():
				tagQuery = "{" + namespaces[tagPrefix] + "}" + tagName
			else:
				tagQuery = tagName

			if parentPrefix in namespaces:
				parentQuery =  "{" + namespaces[parentPrefix] + "}" + parentName
			else:
				parentQuery = parentName

		query = ".//"

		if not parent:
			query = query + tagQuery
		else:
			query = query + parentQuery + "/" + tagQuery


		return self.root.findall(query)


	# TODO
	# def getElementByAttribute()


	def __getPropertyFromProperties(self, properties, key, name, prefix):
		if properties is not None:
			if key in properties.keys():
				for prop in properties[key]:
					if (prop["prefix"] == prefix) and (prop["name"] == name):
						return prop
		return None



	def __getCurveID(self, ring, curveMember):
		curve = ring[curveMember].getchildren()[0]
		return curve.attrib["{http://www.opengis.net/gml/3.2}id"]

	def __getCurvePosList(self, ring, curveMember):
		curve = ring[curveMember].getchildren()[0]
		segment = curve.getchildren()[0]
		lineStringSegment = segment.getchildren()[0]
		posList = lineStringSegment.getchildren()[0]
		pos_list = posList.text.split(" ")
		return pos_list


	def __alkisAnnotate(self, element, uid):
		# tag = self.__getNameFromTag(element.tag, "}")
		children = element.getchildren()
		surface = children[0]
		if "{http://www.opengis.net/gml/3.2}Surface" in surface.tag:
			multiPolygon_id = children[0].attrib["{http://www.opengis.net/gml/3.2}id"]
			self.graph.add((self.ontologyNamespaces["alkis"][uid], self.ontologyNamespaces["alkis"]["position"], self.ontologyNamespaces["alkis"][uid + "_" + "position"]))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "position"], RDF.type, self.ontologyNamespaces["ngeo"]["MultiPolygon"]))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "position"], self.ontologyNamespaces["ngeo"]["id"], Literal(multiPolygon_id)))
			children = surface.getchildren()
			patches = children[0]
			if "{http://www.opengis.net/gml/3.2}patches" in patches.tag:
				children = patches.getchildren()
				polygonPatch = children[0]
				if "{http://www.opengis.net/gml/3.2}PolygonPatch" in polygonPatch.tag:
					self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "polygonMember"], RDF.type, self.ontologyNamespaces["ngeo"]["Polygon"]))

					children = polygonPatch.getchildren()

					for element in children:
						if element.tag in "{http://www.opengis.net/gml/3.2}exterior":
							exterior_children = element.getchildren()
							ring = exterior_children[0]
							if ring.tag in "{http://www.opengis.net/gml/3.2}Ring":
								ring_child = ring.getchildren()
								point_list = []
								linearRing = BNode()
								posList = BNode()
								points = []
								plist = [BNode()]
								for x in range(0, len(ring_child)):
									lat = self.__getCurvePosList(ring_child, x)[0]
									lon = self.__getCurvePosList(ring_child, x)[1]
									utm = UTM(32, "n", float(lat) , float(lon))
									coordinates = utm.toLatLon()
									if x == 0:
										id1 = self.__getCurveID(ring_child, 0)
										id2 = self.__getCurveID(ring_child, len(ring_child)-1)
										point = BNode()
										self.graph.add((point, self.ontologyNamespaces["geo"]["lat"], Literal(str(coordinates[0]))))
										self.graph.add((point, self.ontologyNamespaces["geo"]["long"], Literal(str(coordinates[1]))))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id1)))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id2)))
										self.graph.add((posList, RDF.first, point))
										points.append(point)
										if len(ring_child) > 1:
											self.graph.add((posList, RDF.rest, plist[x]))
										else:
											self.graph.add((posList, RDF.rest, RDF.nil))

									else:
										id1 = self.__getCurveID(ring_child, x-1)
										id2 = self.__getCurveID(ring_child, x)

										point = BNode()
										self.graph.add((point, self.ontologyNamespaces["geo"]["lat"], Literal(str(coordinates[0]))))
										self.graph.add((point, self.ontologyNamespaces["geo"]["long"], Literal(str(coordinates[1]))))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id1)))
										self.graph.add((point, self.ontologyNamespaces["ngeo"]["id"], Literal(id2)))
										points.append(point)
										self.graph.add((plist[x-1], RDF.first, points[x]))


										if (x+1) < len(ring_child):
											plist.append(BNode())
											self.graph.add((plist[x-1], RDF.rest, plist[x]))
										else:
											self.graph.add((plist[x-1], RDF.rest, RDF.nil))
									
									# point_list.append([coordinates[0], coordinates[1], [id1, id2]])
									
								collection.Collection(self.graph,posList)
								self.graph.add((linearRing, RDF.type, self.ontologyNamespaces["ngeo"]["LinearRing"]))
								self.graph.add((linearRing, self.ontologyNamespaces["ngeo"]["posList"], posList))

							self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "polygonMember"], self.ontologyNamespaces["ngeo"]["exterior"], linearRing))
							self.graph.add((self.ontologyNamespaces["alkis"][uid + "_" + "position"], self.ontologyNamespaces["ngeo"]["polygonMember"], self.ontologyNamespaces["alkis"][uid + "_" + "polygonMember"]))

	def __alkisAnnotatePoint(self, element, uid):
		children = element.getchildren()
		point = children[0]
		if "{http://www.opengis.net/gml/3.2}Point" in point.tag:
			point_id = children[0].attrib["{http://www.opengis.net/gml/3.2}id"]
			self.graph.add((self.ontologyNamespaces["alkis"][uid], self.ontologyNamespaces["alkis"]["objektkoordinaten"], self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"]))
			position = point.getchildren()[0].text.split(" ")
			utm = UTM(32, "n", float(position[0]), float(position[1]))
			location = utm.toLatLon()
			# print location
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], RDF.type, self.ontologyNamespaces["ngeo"]["Point"]))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], self.ontologyNamespaces["geo"]["lat"], Literal(str(location[0]))))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], self.ontologyNamespaces["geo"]["lon"], Literal(str(location[1]))))
			self.graph.add((self.ontologyNamespaces["alkis"][uid + "_objektkoordinaten"], self.ontologyNamespaces["ngeo"]["id"], Literal(point_id)))

	def annotate(self, element, depth = 0, uid = "", parent = None, properties = {}, isList = False, mlist = None):
		# print ("==========")
		# print ("%i:%s" % (depth, element.tag))

		# print ("%i:%s" % (depth, element.text))
		# print ("uid: %s" % (uid))
		tag_infos = self.__getTagInfos(element.tag, "}")
		name = tag_infos["name"]
		prefix = tag_infos["prefix"]
		prefix_resolved = self.ontology.ontologyPrefixes[self.ontology.resolveFilePrefix(prefix)]

		if parent is not None:
			parent_infos = self.__getTagInfos(parent.tag, "}")
			parent_name = parent_infos["name"]
			parent_prefix = parent_infos["prefix"]
			parent_prefix_resolved = self.ontology.ontologyPrefixes[self.ontology.resolveFilePrefix(parent_infos["prefix"])]

		# print "Tag = " + tag
		if name == "position":
			self.__alkisAnnotate(element, uid)
			return
		if name == "objektkoordinaten":
			self.__alkisAnnotatePoint(element, uid)
			return


		properties.update({element.tag : self.ontology.verifyCardinalities(self.__getChildNodes(element), tag_infos)})

		if self.ontology.isClass(tag_infos) and (depth == 0):
			# print "---->Class"
			if not uid:
				uid = self.__getIdentifier(element)
			self.graph.add((self.ontologyNamespaces[self.ontology.annotationPrefix][uid], RDF.type, self.ontologyNamespaces[self.ontology.annotationPrefix][name]))


		elif self.ontology.isClass(tag_infos):
			if isList:
				# print "isList"
				subject = self.__forClass(URIRef(self.ontologyNamespaces[self.ontology.annotationPrefix] + uid), URIRef(parent_prefix_resolved + parent_name), URIRef(prefix_resolved + name))
				# print str(subject)
				if subject is not None:
					self.graph.add((subject, RDF.type, URIRef(prefix_resolved + name)))

			else:
				self.graph.add((self.ontologyNamespaces[self.ontology.annotationPrefix][uid + "_" + parent_name], RDF.type, self.ontologyNamespaces[self.ontology.annotationPrefix][name]))


		elif self.ontology.isObjectProperty(tag_infos):
			if self.ontology.checkDomain(tag_infos, self.__getTagInfos(parent.tag, "}"), "objectProperty"):
				# print "Domain is True"
				for child in element:
					if self.ontology.checkRange(tag_infos, self.__getTagInfos(child.tag, "}")):
						prop = self.__getPropertyFromProperties(properties, parent.tag, name, prefix)
						# print "Range is True"
						if prop is not None:
							if prop["valid"] == True:
								if prop["frequency"] > 1:
									# print "is a list"
									subject = self.__getObjectOfLastListItem(URIRef(self.ontologyNamespaces[self.ontology.annotationPrefix] + uid), URIRef(parent_prefix_resolved + parent_name), URIRef(prefix_resolved + name))
									if (URIRef(prefix_resolved + uid), URIRef(prefix_resolved + name), None) not in self.graph:
										# print "doesnt exist"
										list_node = BNode()
										self.graph.add((list_node, RDF.first, BNode()))
										self.graph.add((list_node, RDF.rest, RDF.nil))
										self.graph.add((subject, URIRef(prefix_resolved + name), list_node))
									else:
										# print element.tag + " exists"
										self.graph.remove((subject, RDF.rest, None))

										list_node = BNode()
										self.graph.add((list_node, RDF.first, BNode()))
										self.graph.add((list_node, RDF.rest, RDF.nil))
										self.graph.add((subject, RDF.rest, list_node))

									# print self.ontologyNamespaces[self.ontology.annotationPrefix]
									# print self.__getObjectOfLastListItem(URIRef(self.ontologyNamespaces[self.ontology.annotationPrefix] + uid), URIRef(parent_prefix_resolved + parent_name), URIRef(prefix_resolved + name))
									isList = True
								else:
									if isList:
										# -TODO: if an object property which is a list has another object property which is also a list
										# print "isList"
										# print URIRef(parent_prefix_resolved + parent_name), URIRef(prefix_resolved + name)
										# self.output()
										subject = self.__getObjectOfLastListItem(URIRef(self.ontologyNamespaces[self.ontology.annotationPrefix] + uid), URIRef(parent_prefix_resolved + parent_name), URIRef(prefix_resolved + name))
										# print "subject: " + str(subject)
										self.graph.add((subject, URIRef(prefix_resolved + name), BNode()))


									else:
										self.graph.add((self.ontologyNamespaces[self.ontology.annotationPrefix][uid], self.ontologyNamespaces[self.ontology.annotationPrefix][name], self.ontologyNamespaces[self.ontology.annotationPrefix][uid + "_" + name]))


						else:
							# print "HERE"
							self.graph.add((self.ontologyNamespaces[self.ontology.annotationPrefix][uid], self.ontologyNamespaces[self.ontology.annotationPrefix][name], self.ontologyNamespaces[self.ontology.annotationPrefix][uid + "_" + name]))

						


		elif self.ontology.isDataTypeProperty(tag_infos):
			if self.ontology.checkDomain(tag_infos, parent_infos, "dataTypeProperty"):

				if isList:
					# print "isList"
					subject = self.__forDataTypeProperty(URIRef(self.ontologyNamespaces[self.ontology.annotationPrefix] + uid), URIRef(parent_prefix_resolved + parent_name), URIRef(prefix_resolved + name))
					if isDate(element.text):
						self.graph.add((subject, URIRef(prefix_resolved + name), Literal(element.text, datatype=XSD.date)))
					else:
						self.graph.add((subject, URIRef(prefix_resolved + name), Literal(element.text)))
					
				else:
					for s,p,o in self.graph.triples( (None, None, URIRef(parent_prefix_resolved + parent_name)) ):
						if uid in s:
							if isDate(element.text):
	   							self.graph.add((s, self.ontologyNamespaces[self.ontology.annotationPrefix][name], Literal(element.text, datatype=XSD.date)))
	   						else:
	   							self.graph.add((s, self.ontologyNamespaces[self.ontology.annotationPrefix][name], Literal(element.text)))
			
		else:
			if not self.ontology.isClass(tag_infos):
				self.errors.append("Tag: " + name + " not found in ontology.")


		# for child in element:
		# 	print "\t---->" + child.tag

		# if parent is not None:
		# 	print "Parent: " + parent

		# print (properties)
		parent = element
   			
		# print ("==========")
		for elem in element.getchildren():
			depth += 1
			# print "~~~~~~~~~~~~~~"
			# self.printList(mlist)
			# print "~~~~~~~~~~~~~~"
			self.annotate(elem, depth, uid, parent, properties, isList, mlist)
			depth -= 1

		# print properties


	def output(self, destination = None, format = "turtle"):
		if not destination:
			print self.graph.serialize(format = format)
		else:
			print "Saving to " + destination + "..."
			self.graph.serialize(destination = destination, format = format)
			print "Successfully saved."
		self.graph = Graph()
		self.__addNamespacesToGraph()


	def __getNamespacesFromOntology(self):
		namespaces = {}
		for name in self.ontology.ontologyPrefixes:
			if (name == "owl") or (name == "xsd") or (name == "rdf") or (name == "rdfs"):
				continue
			else:
				namespaces[name] = Namespace(self.ontology.ontologyPrefixes[name])
		return namespaces


	def __addNamespacesToGraph(self):
		for name_space, path in self.ontologyNamespaces.items():
			self.graph.bind(name_space, path)


	def __validateDataLocation(self, filename):
		return os.path.isfile(filename)


	def __getDataPrefix(self):
		for key, value in self.namespaces.iteritems():
			if value == self.baseNamespace:
				return key


	# gets prefix and name for a string
	# prefix and name need to be separated by a separator
	# example: {http://www.adv-online.de/namespaces/adc/gid/6.0}AX_Flurstueck
	# separator would be "}"
	def __getTagInfos(self, tag, separator):
		tag_infos = {}
		
		if separator not in tag:
			tag_infos.update({"prefix" : None}) 
			tag_infos.update({"name" : tag})

		else:
			parantheses = [")", "]", "}"]

			name = tag[tag.find(separator) + 1 : ]

			if separator not in parantheses:
				prefix = tag[: tag.find(separator)]
			else:
				prefix = tag[1: tag.find(separator)]


			tag_infos.update({"prefix" : prefix})
			tag_infos.update({"name" : name})

		return tag_infos


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#|																														|
	def __getIdentifier(self, element):
		for elem in element.getchildren():
			if self.namespaces["gml"] in elem.tag:
				return elem.text
			else:
				return self.__generateUniqueID(element)

	def __generateUniqueID(self, element):
		x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
		return "urn:adv:oid:" + x

#|																														|
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#|																										|

	def __propInDict(self, node, node_list):
		for n in node_list:
			if (node["prefix"] == n["prefix"]) and (node["name"] == n["name"]):
				return True
		return False


	def __getChildNodes(self, element):
		children = []
		child_nodes = element.getchildren()
		for child in child_nodes:
			tag_infos = self.__getTagInfos(child.tag, "}")
			tag_infos.update({"valid" : True})
			# tag_infos.update({"tag" : element.tag})
			if self.__propInDict(tag_infos, children):
				for n in children:
					if (tag_infos["prefix"] == n["prefix"]) and (tag_infos["name"] == n["name"]):
						n["frequency"] +=1
						n["nodes"].append(child)


			else:
				tag_infos.update({"frequency" : 1})
				tag_infos.update({"nodes" : [child]})
				children.append(tag_infos)


		return children
#|																										|
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––



# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#|																																			|

	def __printList(self, liste):
		for s,p,o in self.graph.triples((liste, None, None)):
			print s,p,o
			self.printList(o)

	def __getSubjectsOfObject(self, obj):
		subjects = []
		for s, p, o in self.graph.triples((None, None, obj)):
			subjects.append(s)
		return subjects


	def __subjectIsList(self, subject):
		if (subject, RDF.first, None) in self.graph:
			return True
		return False

	def __listRestIsNil(self, li):
		if (li, RDF.rest, RDF.nil) in self.graph:
			return True
		return False


	def __getListRestSubject(self, first_element):
		# print "getListRestSubject"
		# print "––––––––––––––––––"
		if (first_element, RDF.rest, RDF.nil) in self.graph:
			# print "\t List element is already last"
			# print "–––––––––––––––––––––––––––––––––––"
			return first_element
		else:
			# print "\t List element is not last"
			for s,p,o in self.graph.triples((first_element, RDF.rest, None)):
				# print "\t" + s,p,o
				return self.__getListRestSubject(o)
			# print "–––––––––––––––––––––––––––––––"


	def __getObjectOfLastListItem(self, uid, subject, predicate):
		# print "For ObjectProperty: "
		elements = []
		# if uid == self.__getSuperParent(subject):
		if (None, RDF.type, subject) in self.graph:
			for s,p,o in self.graph.triples((None, None, subject)):
				# print "-" + s,p,o
				if uid == self.__getSuperParent(s):
					elements.append(s)
			# print ""
				
		if len(elements):
			for element in elements:
				subjects = self.__getSubjectsOfObject(element)
				# print "\t" + str(subjects)
				if not len(subjects):
					# print "\tno subjects found for " + str(element) 
					# print "\treturn: " + str(element)
					if (element, predicate, None) in self.graph:
						# print "\tFound " + str(predicate)
						for s,p,o in self.graph.triples((element, predicate, None)):
							# print "\t\t" + s,p,o
							if self.__subjectIsList(o):
								# print "\t\tis a list"
								last_list_item = self.__getListRestSubject(o)
								# print "\t\tlast list item: " + str(last_list_item)
								# print ""
								return last_list_item
							# else:
								# print "\t\tis not a list"

					return element
				else:
					for s in subjects:
						if self.__subjectIsList(s):
							if self.__listRestIsNil(s):
								return element

		# print ""
		return None

	def __forClass(self, uid, object_property, class_uri):
		objects = []
		# print "For Class: " + str(class_uri)
		if (None, object_property, None) in self.graph:
			for s,p,o in self.graph.triples((None, object_property, None)):
				if uid == self.__getSuperParent(o):
					# print "-" + s,p,o
					objects.append(o)

		if len(objects):
			for obj in objects:
				# print "\tobject: " + obj
				if self.__subjectIsList(obj):
					# print "\t" + obj + " is a list"					
					# for s,p,o in self.graph.triples((obj, None, None)):
						# print "\t\t" + s,p,o
					if (obj, RDF.rest, RDF.nil) in self.graph:
						# print "\t\tlast element"
						for s,p,o in self.graph.triples((obj, RDF.first, None)):
							if (o, RDF.type, class_uri) not in self.graph:
								# print "\t\t\treturn: " + o
								return o
							# else:
							# 	print "\t\t\tclass found already"
					else:
						# print "\t\tis not last element"
						last_list_item = self.__getListRestSubject(obj)
						# print "\t\tlast element is: " + str(last_list_item)
						for bs, bp, bo in self.graph.triples((last_list_item, RDF.first, None)):
							# print "\t\t\t" + bs, bp, bo
							if (bo, RDF.type, class_uri) not in self.graph:
								# print "\t\t\treturn: " + bo
								return bo
							# else:
							# 	print "\t\t\tclass found already"

				else:
					# print "\tnot a list"
					if (obj, RDF.type, class_uri) not in self.graph:
						# print "\t\tdoesnt have class"
						for s,p,o in self.graph.triples((None, None, obj)):
							# print "\t\t\t" + s,p,o
							for sub, pred, ob in self.graph.triples((None, None, s)):
								# print "\t\t\t\t" + sub, pred, ob
								if (sub, RDF.rest, RDF.nil):
									# print "\t\t\t\treturn: " + obj
									# print ""
									return obj
						# 	print ""
						# print ""


					# else:
					# 	print "has class, go to next"

				
			# print ""


		# print "-RETURN-"
		return None


	def __forDataTypeProperty(self, uid, subject, predicate):
		# print "For DataTypeProperty: "
		elements = []
		# if uid == self.__getSuperParent(subject):
		if (None, RDF.type, subject) in self.graph:
			for s,p,o in self.graph.triples((None, None, subject)):
				# print "-" + s,p,o
				if uid == self.__getSuperParent(s):
					elements.append(s)
			# print ""
				
		if len(elements):
			for element in elements:
				subjects = self.__getSubjectsOfObject(element)
				if not len(subjects):
					if (element, predicate, None) in self.graph:
						# print "here1"
						abc = 1
				else:
					for s in subjects:
						if self.__subjectIsList(s):
							if self.__listRestIsNil(s):
								# print "here"
								# print element
								return element
							else:
								# print "else"
								rest = self.__getListRestSubject(s)
								# print "rest: " + rest

						else:
							# print "not a list"
							subject_of_object_properties = self.__getSubjectsOfObject(s)
							for subject_of_object_property in subject_of_object_properties:
								if self.__subjectIsList(subject_of_object_property):
									# print "subject of..is list"
									if self.__listRestIsNil(subject_of_object_property):
										# print "is nil"
										return element
									else:
										# print "not nil"
										rest = self.__getListRestSubject(subject_of_object_property)


	def __getSuperParent(self,subject):
		in_loop = False
		val = None

		for s,p,o in self.graph.triples((None, None, subject)):
			in_loop = True
			# print "\t" + str(s) + ", " + str(p) + "," + str(o)
			val = self.__getSuperParent(s)

		if not in_loop:
			return subject
		else:
			return val

		# if not in_loop:
		# 	print "here"
		# 	return subject


	def __getSubject(self, subject, class_name):
		for s,p,o in self.graph.triples((None, None, class_name)):
			print s,p,o
			super_parent = self.__getSuperParent(s)
			if subject == super_parent:
				if (s, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#nil")):
					print "NIL: " + str(s)
				else:
					print self.__getSubject()

#|																																			|
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––



	
	# def __getPrefixFromTag(self, tag, separator = ":"):
	# 	if separator in tag:
	# 		prefix = tag[:tag.find(separator)]
	# 		return prefix
	# 	else:
	# 		return None

	# def __getNameFromTag(self, tag, separator = ":"):
	# 	if separator in tag:
	# 		name = tag[tag.find(separator) + 1 : ]
	# 		return name
	# 	else:
	# 		return tag