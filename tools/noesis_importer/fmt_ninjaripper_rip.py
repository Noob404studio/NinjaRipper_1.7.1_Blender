'''Noesis import plugin. Written by Sammie'''
'''Last Update: 27.01.2013'''
'''Version: 1.18'''

from inc_noesis import *

import noesis
import rapi
import os
import hashlib


RIPVERSION = 4
NOEPY_HEADER = 0xDEADC0DE

g_VertexFormatRecog = 0 # switch to 1 if you want to set the following idx-variables manually. See http://cgig.ru/en/2012/10/ho-to-use-ninja-ripper/ for more details

g_PosX_Idx = 0 # Vertex X
g_PosY_Idx = 1 # Vertex Y
g_PosZ_Idx = 2 # Vertex Z
g_NormX_Idx = 3 # Normal X
g_NormY_Idx = 4 # Normal Y
g_NormZ_Idx = 5 # Normal Z
g_Tc0_U_Idx = 6 # UVmap U
g_Tc0_V_Idx = 7 # UVmap V
g_Tc0_UF_Idx = -1 # UVmap U Flag
g_Tc0_VF_Idx = -1 # UVmap V Flag
g_swapNormals = 0 # 0/1
g_vScale = 1 # 1-100
g_flipUV = 1 # 1/-1
g_scan_gamelist = 1 # 0/1

display_debug_messages = 0

game_list = {
	'de00794b7e6bbcce48f778a01df91e18': {'name':'Alan Wake\'s American Nightmare','data':[0,1,2,7,8,9,11,12,-1,-1], 'func':'div_4096'}, # 72
	'03d01c16db9bda739bf04780e0e64cde': {'name':'Automobili Lamborghini (N64)','data':[0,1,2,3,4,5,7,8,-1,-1]}, # 52
	'631896c9e91075cdb41f53659f100ff3': {'name':'Battlefield 3','data':[0,1,2,12,13,14,20,21,-1,-1]}, # 96
	'a77711c6bd147c4e8f363a3442713906': {'name':'Battlefield 3','data':[0,1,2,16,17,18,24,25,-1,-1]}, # 112
	'86aa9fdaac04ffa0f2344c6c276a4a6d': {'name':'Batman Arkham City','data':[16,17,18,4,5,6,19,20,-1,-1],'angle':[0,90,90],'rotate':'YZ', 'swap':'X'}, # 124
	'c2d309a064e26fefc6e580d19394d7d8': {'name':'Bionic Commando','data':[0,1,2,13,14,15,3,4,-1,-1],'rotate':'YZ'}, # 108
	'03d2f4571536fe31dbbcac95434f59e8': {'name':'Call Of Duty 4','data':[0,1,2,12,13,14,8,9,-1,-1]}, # 80, unknown Normal/UV Format
	'f57950fb31f0d25cc3ab09c37641ffc3': {'name':'Call of Duty: Black Ops 2','data':[0,1,2,10,11,12,8,9,-1,-1],'angle':[0,90,90],'swap':'X','rotate':'YZ'}, # 72	
	'beced9aa9c6fc8d794a353ef977f9041': {'name':'Crysis 2','data':[0,1,2,4,5,6,8,9,-1,-1],'angle':[0,90,90],'rotate':'YZ'}, # 128
	'b7bf6a2f2803dc34c6237ed4510ea5ee': {'name':'Deus Ex: Human Revolution','data':[23,24,25,4,5,6,19,20,-1,-1],'rotate':'YZ', 'func':'mul_16'}, # 120
	'f6a2d7730a6bf30da90ff2a1d736def6': {'name':'Diablo 3','data':[0,1,2,3,4,5,15,17,16,18],'angle':[0,180,0],'func':'bit_128'}, # 92
	'2dabf24b9f4122fd01c51cc25e914d6d': {'name':'Diablo 3','data':[0,1,2,3,4,5,15,17,16,18],'angle':[0,180,0],'func':'bit_128'}, # 104
	'2e7a8e4b8d0a3489271926455e0259b9': {'name':'Diablo 3','data':[0,1,2,3,4,5,15,17,16,18],'angle':[0,180,0],'func':'bit_128'}, # 120
	'6e7a202e7d5ffbd0885e9589eea83cdc': {'name':'Dead Island','data':[0,1,2,13,14,15,11,12,-1,-1],'func':'div_4096'}, # 84
	'8ecd8720c4888b7cae848a9650d40d56': {'name':'Dragon Age','data':[21,22,23,10,11,12,0,1,-1,-1],'angle':[0,90,90],'rotate':'YZ'}, # 100
	'fdb87e910b6c95f420be7bcf3526e7b9': {'name':'Dragon Age','data':[0,1,2,14,15,16,4,5,-1,-1],'angle':[0,90,90],'rotate':'YZ'}, # 104
	'92747ffb440ca8719757403795324db5': {'name':'Driv3r','data':[0,1,2,3,4,5,6,7,-1,-1], 'swap':'X'}, # 48	
	'7dd0ce319221e92cec0b602c78c6cc89': {'name':'Driv3r','data':[0,1,2,3,4,5,6,7,-1,-1], 'swap':'X'}, # 60
	'c0c216144ab0f8aafac481fd6f199185': {'name':'Driv3r','data':[0,1,2,3,4,5,6,7,-1,-1], 'swap':'X'}, # 72	
	'ca105dac5d4e24ded28090417a061b7f': {'name':'Duke Nukem Forever','data':[0,1,2,4,5,6,12,13,-1,-1],'angle':[0,180,0]}, # 60
	'0408b389444ef983d996676a42bd7f05': {'name':'F.E.A.R.','data':[0,1,2,3,4,5,6,7,-1,-1]}, # 88
	'9d4010f4dcd7c046b4c408df90262135': {'name':'Grand Theft Auto 4','data':[0,1,2,11,12,13,18,19,-1,-1],'angle':[0,90,90],'rotate':'YZ'}, # 96	
	'6efad5b73e6be9eb327e7d25bf04a52a': {'name':'Guild Wars 2','data':[0,1,2,11,12,13,23,24,-1,-1],'rotate':'ZY',}, # 100
	'1100a44c2b9f03754ce80b01a3aa93f6': {'name':'Hitman Absolution','data':[0,1,2,3,4,5,19,20,-1,-1],'rotate':'YZ', 'func': 'half_shift'}, # 84
	'9714e84fa0f39f6d3fa514aeef193276': {'name':'Hitman Absolution','data':[0,1,2,4,5,6,24,25,-1,-1],'rotate':'YZ', 'func': 'half_shift'}, # 120
	'07180ef3ce4b9239e90eaa1719cf3865': {'name':'Lara Croft And The Guardian Of Light','data':[0,1,2,3,4,5,15,16,-1,-1],'rotate':'YZ', 'func':'div_2048'}, # 72
	'5bce14cf9f859d88ba3330877698077b': {'name':'Lego: The Lord Of The Rings','data':[0,1,2,16,17,18,24,25,-1,-1],'angle':[0,90,90]}, # 104
	'76f32e763ad9e7caf3cc2583405e47ed': {'name':'Mafia','data':[2,1,0,3,4,5,7,8,-1,-1],'angle':[0,90,90],'swap':'X'}, # 36
	'48afceacb2e3433b1846eeea6a4d959f': {'name':'Mafia','data':[2,1,0,3,4,5,7,8,-1,-1],'angle':[0,90,90],'swap':'X'}, # 44
	'1f48f3a24597f97d542285ec02ed8163': {'name':'Max Payne 3','data':[0,1,2,11,12,13,7,8,-1,-1],'angle':[0,180,0]},  # 72
	'1fa031f828e53b57d497fb5ebcaaa2ff': {'name':'Metro 2033','data':[0,1,2,4,5,6,24,25,-1,-1],'func':'div_2048'}, # 104
	'700dbcfadb9e80cb55b1eddb78fc53e1': {'name':'Need For Speed: Hot Pursuit','data':[0,1,2,4,5,6,9,10,-1,-1],'swap':'X'}, # 76	
	'4b7893fe9e2afa66f8811e2d3c9c0948': {'name':'Need For Speed: Most Wanted'}, # 104, corrupt mesh
	'ccae7d946e711d21eebc3393cb249e28': {'name':'Painkiller Recurring Evil ','data':[0,1,2,3,4,5,6,7,-1,-1]}, # 60
	'daa19a27374f61e261513182d0500fec': {'name':'Prototype','data':[0,1,2,4,5,6,16,17,-1,-1],'angle':[0,90,90]}, # 72
	'7d17fe2680bc9c41b3c3b31a7f244a9f': {'name':'Shadow Harvest','data':[0,1,2,3,4,5,16,17,-1,-1]}, # 100
	'ad365cb0f859a8a1623f0b53df41c576': {'name':'Sonic Generations','data':[0,1,2,3,4,5,12,13,-1,-1]}, # 128
	'43254b251a9ede481910933be959a38f': {'name':'Street Fighter IV','data':[0,1,2,3,4,5,6,7,-1,-1],'angle':[0,90,90],'swap':'X',}, # 88
	'e491e0051c71095c379cc328091dddaa': {'name':'Serious Sam 3','data':[0,1,2,3,4,5,10,11,-1,-1],'angle':[0,90,90]}, # 96
	'd3efc7346047429f92f7be3a2d52ed39': {'name':'Serious Sam 3','data':[0,1,2,3,4,5,10,11,-1,-1],'angle':[0,90,90]}, # 104
	'90c80e47a362831bedc43ed5f487d97b': {'name':'Singularity','data':[0,1,2,7,8,9,15,16,-1,-1],'angle':[0,180,0],'swap':'X'}, # 132
	'a0bd3127924b17f152742cc79821509e': {'name':'Sonic 4','data':[0,1,2,3,4,5,6,7,-1,-1], 'swap': 'X'}, # 32
	'a22c3914ee21dfc89b3a9fbf56702335': {'name':'Super Mario 64 / Zelda: Ocarina Of Time (N64)','data':[0,1,2,-1,-1,-1,7,8,-1,-1],'func':'div_256'}, # 36	
	'98bd9525f5c7261c69f00def268a2a70': {'name':'Super Mario Galaxy / Zelda Wind Waker','data':[0,1,2,3,4,5,10,11,-1,-1],'swap': 'X'}, # 48
	'b1f60f3d241bd2cc47f224f53f09b74b': {'name':'Super Smash Brothers','data':[0,1,2,3,4,5,11,12,-1,-1],'func':'div_256'}, # 52
	'05b56e87c8e10365f6332bcdc3de15aa': {'name':'The Walking Dead','data':[0,1,2,12,13,14,3,4,-1,-1]}, # 80
	'26f54c5cee1c391e5a5fdb54ddc4e7dd': {'name':'Tomb Raider: Underworld','data':[0,1,2,3,4,5,15,16,-1,-1],'rotate':'YZ','func':'div_2048'}, # 116	
	'caa84a4e7ae1867859523acaedebbf62': {'name':'Trine 2','data':[0,1,2,4,5,6,10,11,10,11],'func':'trine2', 'func': ''}, # 48 , unknown UV Format
	'fb013b0aaa8324892368ee5a49519377': {'name':'Trine 2','data':[0,1,2,4,5,6,8,9,10,11],'func':'trine2', 'func': ''}, # 64 , unknown UV Format
	'aceaf7db00c20836759c16fe29666d5b': {'name':'Tropico 3','data':[0,1,2,-1,-1,-1,4,5,6,7],'func':'div_4096'}, # 64
	'bf93d5894c5e18f50620133531913028': {'name':'Tropico 3','data':[0,1,2,-1,-1,-1,4,5,6,7],'func':'div_4096'}, # 80
	'fc1c51098b973a14ba78263209a05a6a': {'name':'Wolfenstein 3D','data':[0,1,2,4,5,6,17,18,-1,-1],'swap':'X'}, # 76	
}

game_list_uv_functions = {
	'bit_128': lambda c,value,flag: (0.5/255*value) - ((128-flag)*0.5),
	'half_shift': lambda c,value,flag: ((value*0.5)+0.5),
	'div_4096': lambda c,value,flag: (value/4096),
	'div_2048': lambda c,value,flag: (value/2048),
	'div_1024': lambda c,value,flag: (value/1024),
	'div_256': lambda c,value,flag: (value/256),
	'mul_2': lambda c,value,flag: (value*2),
	'mul_16': lambda c,value,flag: (value*16),
	'mul_x': lambda c,value,flag: (value*32),
	'trine2': lambda c,value,flag: (0),
}

def registerNoesisTypes():

	if display_debug_messages == 1:
		noesis.logPopup()
	
	handle = noesis.register("NinjaRipper", ".rip")
	noesis.setHandlerTypeCheck(handle, noepyCheckType)
	noesis.setHandlerLoadModel(handle, noepyLoadModel)
	return 1

def noepyCheckType(data):
	
	if len(data) < 8:
		return 0
	bs = NoeBitStream(data)
	if bs.readUInt() != NOEPY_HEADER:
		return 0
	version = bs.readUInt()
	if version != RIPVERSION:
		noesis.messagePrompt("Wrong file version: need version " + str(RIPVERSION) + " but version " + str(version) + " found")
		return 0
	return 1
	

def noepyLoadModel(data, mdlList):

	ctx = rapi.rpgCreateContext()
	filename = rapi.getLocalFileName(rapi.getInputName())
	parser = SanaeParser(data, filename)
	parser.parse_file()
	mdl = rapi.rpgConstructModel()
	mdl.setModelMaterials(NoeModelMaterials(parser.texList, parser.matList))
	mdlList.append(mdl)	
	return 1


class SanaeParser(object):
	
	def __init__(self, data, name=""):	

		self.inFile = NoeBitStream(data)

		self.numVerts = 0
		self.numIdx = 0
		self.numFaces = 0
		self.BlockSize = 0
		self.TextureFilesCnt = 0
		self.ShaderFilesCnt = 0
		self.VertexAttributesCnt = 0
		self.texList = []
		self.matList = []
		self.shadList = []
		self.vertBuff = bytes()
		self.idxBuff = bytes()
		self.filename = name
		self.ShaderFiles = []
		self.TextureFiles = []
		self.hasNormals = 0
		self.hashTag = ""
		self.unpackFormat = ""
		self.PosX_Idx = 0
		self.PosY_Idx = 1
		self.PosZ_Idx = 2
		self.NormX_Idx = 3
		self.NormY_Idx = 4
		self.NormZ_Idx = 5
		self.Tc0_U_Idx = 6
		self.Tc0_V_Idx = 7
		self.Tc0_UF_Idx = 8
		self.Tc0_VF_Idx = 9
		self.swapNormals = 0
		self.flipUV = 1
		self.vScale = 1
		

	def build_mesh(self):
			
		rapi.rpgSetName(self.filename)
		rapi.rpgBindPositionBufferOfs(self.vertBuff, noesis.RPGEODATA_FLOAT, 32, 0)
		if self.hasNormals: rapi.rpgBindNormalBufferOfs(self.vertBuff, noesis.RPGEODATA_FLOAT, 32, 12)
		rapi.rpgBindUV1BufferOfs(self.vertBuff, noesis.RPGEODATA_FLOAT, 32, 24)

		if len(self.matList) > 0:
			material = self.matList[0]
			rapi.rpgSetMaterial(material.name)

		rapi.rpgCommitTriangles(self.idxBuff, noesis.RPGEODATA_UINT, self.numIdx, noesis.RPGEO_TRIANGLE, 1)

	
	def uv_parser(self, c, uv, flag):
	
		return float(uv)
		
		
	def pos_parser(self, vx, vy, vz):
	
		if self.hashTag == 'fb013b0aaa8324892368ee5a49519377':
			vy *= 3
			vz /= 3
			
		if self.hashTag == '9714e84fa0f39f6d3fa514aeef193276' or self.hashTag == '03d01c16db9bda739bf04780e0e64cde':
			vy /= 3
			vx /= 3
			

		vx *= self.vScale
		vy *= self.vScale
		vz *= self.vScale
			
		return [vx, vy, vz]
		
		
	def norm_parser(self, nx, ny, nz):
		
		if self.hasNormals == 0:
			self.hasNormals = 0 if (nx == 0 and ny == 0 and nz == 0) else 1
			
		if self.swapNormals == 1:
			nx *= -1
			ny *= -1
			nz *= -1
				
		return [nx, ny, nz]
		
		
	def scan_game_list(self):

		if self.hashTag in game_list:
			options = game_list[self.hashTag]
			
			print ("'" + options['name'] + "' Model deteced")

			if 'data' in options and len(options['data']) == 10:
				self.PosX_Idx = options['data'][0]
				self.PosY_Idx = options['data'][1]
				self.PosZ_Idx = options['data'][2]
				self.NormX_Idx = options['data'][3]
				self.NormY_Idx = options['data'][4]
				self.NormZ_Idx = options['data'][5]
				self.Tc0_U_Idx = options['data'][6]
				self.Tc0_V_Idx = options['data'][7]
				self.Tc0_UF_Idx = options['data'][8]
				self.Tc0_VF_Idx = options['data'][9]
			
				self.flipUV = -1 if 'flipUV' in options and options['flipUV'] == -1 else 1
		
				self.parse_matrix(options)

				if 'func' in options and options['func'] in game_list_uv_functions:
					self.uv_parser = game_list_uv_functions[options['func']]

				if 'angle' in options and len(options['angle']) == 3:
					rapi.setPreviewOption("setAngOfs", ' '.join( map( str, options['angle'])))
			else:
				print("Invalid Data-Format")
		else:
			print ("Game Model not found. Using automatic detection")
			
			
	def parse_matrix(self, options):
	
		trans = NoeMat43((NoeVec3((1, 0, 0)),
						NoeVec3((0, 1, 0)),
						NoeVec3((0, 0, 1)),
						NoeVec3((0, 0, 0))))
	
		if 'rotate' in options:
			if options['rotate'] == 'ZY':
				trans = NoeMat43((NoeVec3((1, 0, 0)),
								NoeVec3((0, 0, -1)),
								NoeVec3((0, 1, 0)),
								NoeVec3((0, 0, 0))))
				
			elif options['rotate'] == 'YZ':
				trans = NoeMat43((NoeVec3((1, 0, 0)),
								NoeVec3((0, 0, 1)),
								NoeVec3((0, -1, 0)),
								NoeVec3((0, 0, 0))))

		if 'swap' in options:
			if options['swap'] == 'X':
				self.swapNormals = 1
				rapi.rpgSetOption(noesis.RPGOPT_TRIWINDBACKWARD, 1)

		rapi.rpgSetTransform(trans)
		
		
	def set_attributes(self):

		self.PosX_Idx = int(g_PosX_Idx)
		self.PosY_Idx = int(g_PosY_Idx)
		self.PosZ_Idx = int(g_PosZ_Idx)
		self.NormX_Idx = int(g_NormX_Idx)
		self.NormY_Idx = int(g_NormY_Idx)
		self.NormZ_Idx = int(g_NormZ_Idx)
		self.Tc0_U_Idx = int(g_Tc0_U_Idx)
		self.Tc0_V_Idx = int(g_Tc0_V_Idx)
		self.Tc0_UF_Idx = int(g_Tc0_UF_Idx)
		self.Tc0_VF_Idx = int(g_Tc0_VF_Idx)
		self.vScale = g_vScale if g_vScale >= 1 and g_vScale <= 100 else 1
		self.flipUV = -1 if g_flipUV == -1 else 1
		
		if g_swapNormals == 1:
			self.parse_matrix({'swap': 'X'})
			
		
	def is_in_range(self, value, limit):
	
		return 1 if 0 <= value < limit else 0
	
	
	def parse_faces(self):

		self.idxBuff +=  self.inFile.readBytes(self.numIdx * 4)

		
	def parse_vertices(self):
				
		VertexBlocks = len(self.unpackFormat)
		
		DataBuffer = []

		for k in range(self.numVerts+1):

			vertexBufferBytes = self.inFile.readBytes(self.BlockSize)
			vertexBufferList = struct.unpack(self.unpackFormat, vertexBufferBytes)
			
			vx = vertexBufferList[self.PosX_Idx] if self.is_in_range(self.PosX_Idx,VertexBlocks) else 0
			vy = vertexBufferList[self.PosY_Idx] if self.is_in_range(self.PosY_Idx,VertexBlocks) else 0
			vz = vertexBufferList[self.PosZ_Idx] if self.is_in_range(self.PosZ_Idx,VertexBlocks) else 0
			nx = vertexBufferList[self.NormX_Idx] if self.is_in_range(self.NormX_Idx,VertexBlocks) else 0
			ny = vertexBufferList[self.NormY_Idx] if self.is_in_range(self.NormY_Idx,VertexBlocks) else 0
			nz = vertexBufferList[self.NormZ_Idx] if self.is_in_range(self.NormZ_Idx,VertexBlocks) else 0
			tu = vertexBufferList[self.Tc0_U_Idx] if self.is_in_range(self.Tc0_U_Idx,VertexBlocks) else 0
			tv = vertexBufferList[self.Tc0_V_Idx] if self.is_in_range(self.Tc0_V_Idx,VertexBlocks) else 0
			tu_flag = vertexBufferList[self.Tc0_UF_Idx] if self.is_in_range(self.Tc0_UF_Idx,VertexBlocks) else 0
			tv_flag = vertexBufferList[self.Tc0_VF_Idx] if self.is_in_range(self.Tc0_VF_Idx,VertexBlocks) else 0

			tu = self.uv_parser('U',tu,tu_flag);
			tv = self.uv_parser('V',tv,tv_flag) * self.flipUV;
			
			vx,vy,vz = self.pos_parser(vx,vy,vz)
			nx,ny,nz = self.norm_parser(nx,ny,nz)

			vertexData = [vx,vy,vz,nx,ny,nz,tu,tv]

			self.vertBuff += struct.pack("8f", *vertexData)
		
	
	def parse_textures(self):

		basename = rapi.getExtensionlessName(self.filename)
		basepath = rapi.getDirForFilePath(rapi.getInputName())
		
		Tex_Basename = basename.replace('Mesh','Tex')
		
		diffTex = basepath + Tex_Basename + "_diff.dds"
		normTex = basepath + Tex_Basename + "_norm.dds"
		specTex = basepath + Tex_Basename + "_spec.dds"

		if rapi.checkFileExists(diffTex):
			material = NoeMaterial(basename + "_diffuse", diffTex)
			material.setFlags(noesis.NMATFLAG_TWOSIDED)
			self.TextureFiles.append('Diffuse: ' + diffTex)
			if (rapi.checkFileExists(normTex)):
				material.setNormalTexture(normTex)
				self.TextureFiles.append('Normal: ' + normTex)
			if (rapi.checkFileExists(specTex)):
				material.setSpecularTexture(specTex)
				self.TextureFiles.append('Specular: ' + specTex)
			self.matList.append(material)

		# Read Textures Block
		if self.TextureFilesCnt > 0:
			for i in range(self.TextureFilesCnt):
				TexFile = self.inFile.readString()
				TexFilePath = rapi.getDirForFilePath(rapi.getInputName()) + "/" + TexFile
				if (rapi.checkFileExists(TexFilePath)):
					self.TextureFiles.append(TexFile)
					material = NoeMaterial('mat' + str(i), str(TexFile))
					material.setFlags(noesis.NMATFLAG_TWOSIDED)
					self.matList.append(material)
	
	
	def parse_shaders(self):
	
		# Read Shaders Block
		if self.ShaderFilesCnt > 0:
			for i in range(self.ShaderFilesCnt):
				ShaderFile = self.inFile.readString();
				self.ShaderFiles.append(ShaderFile)
	
			
	def parse_file(self):
		
		idstring = self.inFile.readBytes(4)
		version = self.inFile.readUInt()

		self.numFaces = self.inFile.readUInt()
		self.numVerts = self.inFile.readUInt()
		self.BlockSize = self.inFile.readUInt()
		self.TextureFilesCnt = self.inFile.readUInt()
		self.ShaderFilesCnt = self.inFile.readUInt()
		self.VertexAttributesCnt = self.inFile.readUInt()
		self.numIdx = self.numFaces * 3
		
		if display_debug_messages == 1:
			print("numFaces: " + str( self.numFaces) + "\n"
			"numIdx: " + str( self.numIdx) + "\n"
			"numVerts: " + str( self.numVerts) + "\n"
			"BlockSize: " + str( self.BlockSize) + "\n"
			"VertexAttributesCnt: " + str( self.VertexAttributesCnt))
		
		VertexAttribList = []

		TempPosIdx = 0
		TempNormalIdx = 0
		TempTexCoordIdx = 0
				
		SemanticOptions = {"POSITION":1, "NORMAL":2, "TEXCOORD":4, "COLOR":8, "TANGENT":16, "BINORMAL":32, "BLENDINDCES":64, "BLENDWEIGHT":128}

		Hash = hashlib.md5()

		for i in range(self.VertexAttributesCnt):
			Semantic = self.inFile.readString()
			SemanticIndex = self.inFile.readUInt()
			Offset = self.inFile.readUInt()
			Size   = self.inFile.readUInt()
			TypeMapElements = self.inFile.readUInt()
			
			TypeElementCharArray = []
	
			# Map Element Types
			TypeElementStruct = ['f','L','l']
			TypeElementIndices = struct.unpack(str(TypeMapElements)+"L", self.inFile.readBytes(TypeMapElements*4))
			for TypeElementIdx in TypeElementIndices:
				TypeElementChar = TypeElementStruct[TypeElementIdx] if TypeElementIdx <= 2 else 'L'
				TypeElementCharArray.append(TypeElementChar)
				self.unpackFormat += TypeElementChar				
			
			VertexAttribList.append([Semantic,SemanticIndex,Offset,Size,TypeElementCharArray])
					
			if display_debug_messages == 1:
				print("Semantic: " + str( Semantic) +
				" | SemanticIndex: " + str(SemanticIndex) +
				" | Offset: " + str(Offset) +
				" | Size: " + str(Size) +
				" | TypeElementCharArray: [" + ','.join( map( str, TypeElementCharArray ) ) +  "]")

			if g_VertexFormatRecog == 0:
				
				if Semantic == "POSITION":
					if TempPosIdx == 0:
						self.PosX_Idx = int(Offset / 4)
						self.PosY_Idx = self.PosX_Idx + 1
						self.PosZ_Idx = self.PosX_Idx + 2
						
						TempPosIdx = 1
				
				elif Semantic == "NORMAL":
					if TempNormalIdx == 0:
						self.NormX_Idx = int(Offset / 4)
						self.NormY_Idx = self.NormX_Idx + 1
						self.NormZ_Idx = self.NormX_Idx + 2
						
						TempNormalIdx = 1
				
				elif Semantic == "TEXCOORD":
					if TempTexCoordIdx == 0:
						self.Tc0_U_Idx = int(Offset / 4)
						self.Tc0_V_Idx = self.Tc0_U_Idx + 1
						
						TempTexCoordIdx = 1
				
			Bit = SemanticOptions[Semantic] if Semantic in SemanticOptions else 0
			
			# Create Hash for Game-Model-Typ
			GameHash = (str.join("", ("%02x" % i for i in [Bit,Offset,TypeElementIdx])))
			Hash.update(GameHash.encode('utf-8'))
			

		self.hashTag = Hash.hexdigest()
		print ("Model-Hash: " + str(self.hashTag))
		
		if g_VertexFormatRecog == 0: # Automatic Dectection
			# Overwrite default TexCoord if double float found
			for VertexAttribData in VertexAttribList:
				Semantic = VertexAttribData[0]
				SemanticIndex = VertexAttribData[1]
				Offset = VertexAttribData[2]
				Size   = VertexAttribData[3]
				VertexAttributes = ''.join(map(str, VertexAttribData[4]))

				if Semantic == "TEXCOORD" and VertexAttributes == "ff":
					self.Tc0_U_Idx = int(Offset / 4)
					self.Tc0_V_Idx = self.Tc0_U_Idx+1
					break
			
			if g_scan_gamelist == 1:
				self.scan_game_list()
			
		else: # Set Manual Attributes
			self.set_attributes()

		self.parse_textures()
		self.parse_shaders()
		self.parse_faces()
		self.parse_vertices()
		self.build_mesh()
			
		if display_debug_messages == 1:
			print (
			"Vertices: " + str(self.PosX_Idx) + "|" + str(self.PosY_Idx) + "|" + str(self.PosZ_Idx) + "\n"
			"Normals: " + str(self.NormX_Idx) + "|" + str(self.NormY_Idx) + "|" + str(self.NormZ_Idx) + "\n"
			"UV: " + str(self.Tc0_U_Idx) + "|" + str(self.Tc0_V_Idx))
			if len(self.TextureFiles): print ("Textures:\n" + "\n".join(map(str, self.TextureFiles)))
			if len(self.ShaderFiles): print ("Shaders:\n" + "\n".join(map(str, self.ShaderFiles)))