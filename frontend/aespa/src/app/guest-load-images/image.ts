export interface Image {
  tags: Tag[];
  directoryPath: string;
  imageId: number;
  imagePath: string;
}

export interface Tag {
  tag_id: number;
  name: string;
}
