from requests import Session
from aiohttp import ClientSession
from json import loads

class Manga():
  def __init__(self, manga_id, session=Session(), async_session=ClientSession(), **kwargs):
    self.id = manga_id
    self.session = session
    self.async_session
    self.populated = False if not kwargs else True
    self.valid = True
    self.url = 'https://mangadex.org/api/manga/{}'.format(self.id)
    self.attr_list = ['session', 'id', 'populated', 'valid', 'url']

    for attr in kwargs.keys():
      setattr(self, attr, kwargs[attr])
      self.attr_list.append(attr)

  async def async_populate(self):
    async with self.async_session.get(self.url) as response:
      text = await response.text()
    self.json = loads(text)
    self.status = self.json['status']
    self.attr_list.append('status')

    if self.json['status'] == 'OK':
      self.valid = True
      self.populated = True

      self.chapters = self.json['chapter']
      self.attr_list.append('chapters')

      for attr in self.json['manga'].keys():
        setattr(self, attr, self.json['manga'][attr])
        self.attr_list.append(attr)
      
      return self
    else:
      self.valid = False
      self.populated = True
      return self
    
  
  def populate(self):
    self.json = loads(self.session.get(self.url).content)
    self.status = self.json['status']
    self.attr_list.append('status')

    if self.json['status'] == 'OK':
      self.valid = True
      self.populated = True

      self.chapters = self.json['chapter']
      self.attr_list.append('chapters')

      for attr in self.json['manga'].keys():
        setattr(self, attr, self.json['manga'][attr])
        self.attr_list.append(attr)
      
      return self
    else:
      self.valid = False
      self.populated = True
      return self
  
  def get_chapters(self):
    if self.valid and self.populated:
      return self.chapters
    elif self.valid and not self.populated:
      self.populate()
      if self.valid:
        return self.chapters
      else:
        return None
    else:
      return None