from requests_html import HTMLSession

class Manga():
  def __init__(self, manga_id, session=HTMLSession(), **kwargs):
    for attr in kwargs.keys():
      setattr(self, attr, kwargs[attr])
    
    self.id = manga_id
    self.session = session
    self.populated = False if not kwargs else True
    self.valid = True
    self.url = 'https://mangadex.org/api/manga/{}'.format(self.id)
  
  def populate(self):
    self.json = self.session.get(self.url).json()

    if self.json['status'] == 'OK':
      self.valid = True
      self.populated = True

      self.chapters = self.json['chapter']
      for attr in self.json['manga'].keys():
        setattr(self, attr, self.json['manga'][attr])
      
      return self
    else:
      self.valid = False
      self.populated = True
      self.status = self.json['status']
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