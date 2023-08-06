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
    self.attr_list = ['session', 'async_session', 'id', 'populated', 'valid', 'url']

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
      chapters = []
      for chapter_id in self.chapters.keys():
        chapters.append(Chapter(chapter_id, session=self.session, async_session=self.async_session, **self.chapters[chapter_id]))
      return chapters
    elif self.valid and not self.populated:
      self.populate()
      if self.valid:
        chapters = []
      for chapter_id in self.chapters.keys():
        chapters.append(Chapter(chapter_id, session=self.session, async_session=self.async_session, **self.chapters[chapter_id]))
        return chapters
      else:
        return None
    else:
      return None

class Chapter():
  def __init__(self, chapter_id, session=Session(), async_session=ClientSession(), **kwargs):
    self.id = chapter_id
    self.session = session
    self.async_session
    self.populated = False if not kwargs else True
    self.valid = True
    self.url = 'https://mangadex.org/api/chapter/{}'.format(self.id)
    self.attr_list = ['session','async_session', 'id', 'populated', 'valid', 'url']

    for attr in kwargs.keys():
      setattr(self, attr, kwargs[attr])
      self.attr_list.append(attr)
  
  async def async_populate(self):
    async with self.async_session.get(self.url) as response:
      text = await response.text()
    self.json = loads(text)

    for attr in self.json.keys():
      setattr(self, attr, self.json[attr])
      self.attr_list.append(attr)
    if 'page_array' in self.attr_list:
      self.pages = self.page_array
      self.attr_list.append('pages')

    if self.status != 'OK':
      self.valid = False
    
    self.populated = True

    return self
  
  def populate(self):
    self.json = loads(self.session.get(self.url).content)

    for attr in self.json.keys():
      setattr(self, attr, self.json[attr])
      self.attr_list.append(attr)
    if 'page_array' in self.attr_list:
      self.pages = self.page_array
      self.attr_list.append('pages')

    if self.status != 'OK':
      self.valid = False
    
    self.populated = True

    return self
  
  def get_pages(self):
    if self.valid and self.populated:
      return self.pages
    elif self.valid and not self.populated:
      self.populate()
      if self.valid:
        return self.pages
      else:
        return None
    else:
      return None