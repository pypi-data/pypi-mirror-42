# -*- coding: utf-8 -*-
from .errors import *
from .image import NaeginImage

import aiohttp

class Client:
    '''API Wrapper para Naeg.in

    - Descrição:
        Cria uma instância

    - Parâmetros:
        token : str
        (Token fornecido para usar a API)
    '''
    def __init__(self, token):
        if not isinstance(token, str):
            raise InvalidArgument('Tokens devem ser strings')

        self.url = 'https://api.naeg.in/{endpoint}?token=' + token

    async def get_all_tags(self):
        '''API Wrapper para Naeg.in

        - Descrição:
            Retorna todas as tags disponíveis em uma list
        '''
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url.format(endpoint='tags')) as r:
                if r.status != 200:
                    raise InvalidResponse('Falha na requisição: Código inválido retornado')
            
                data = await r.json()
                if data['erro']:
                    raise InvalidArgument(data['mensagem'])
                
                return data['tags']

    async def get_random(self, tag, **kwargs):
        '''API Wrapper para Naeg.in

        - Descrição:
            Busca e retorna o link de uma imagem com a tag fornecida

        - Parâmetros:
            tag : str
            (Usada para buscar imagens)

            nsfw : bool (opcional)
            (Especifica se a API deve retornar apenas resultados NSFW ou não)

            gif : bool (opcional)
            (Define se a API deve retornar apenas imagens animadas ou não)
        '''
        url = self.url.format(endpoint='img') + f'&tag={tag}'
        for parameter, value in kwargs.items():
            url += f'&{parameter}={value}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status != 200:
                    raise InvalidResponse('Falha na requisição: Código inválido retornado')
            
                data = await r.json()
                if data['erro']:
                    raise InvalidArgument(data['mensagem'])
            
                return NaeginImage(**data)