# -*- coding: utf-8 -*-
from package.kb import GConceptNetCS
from package.sent import SentParser, SentSimi, SentMaker, join_sents
from package.qa import MaskedQA

q = 'Elephants like to eat [MASK].'

# 解析问题中的实体
# TODO: 优化自动机代码，提高词典的解析速度；当前为python代码，构建树形结构速度慢。
parser = SentParser()
entity = parser.parse(q)
print('Parsing sentence:', entity)

# 链接至常识图谱
# TODO: 增加语义相似匹配代码，当前为字符匹配，默认为小写
kb = GConceptNetCS('192.168.10.174')
context = []
for e in entity:
    context.extend(kb.query(e))
print('Context triple:', context)

# 将检索到的三元组组合成自然语言
maker = SentMaker()
context = [maker.lexicalize(triple) for triple in context]
print('Context sentence:', context)

context_sim = SentSimi()
context = context_sim.lookup(q, context, k=5)
print('Query-related sentence:', context)

engine = MaskedQA('roberta-large')
q = q.replace('[MASK]', engine.mask_token)
context = join_sents(context)
result = engine(q, context)

print(result)
