from dataclasses import dataclass
import pandas as pd

@dataclass
class CocoFrame:
    # has to be dealt with separately
    empty_frames: List[str]
    annotations_df: pd.core.frame.DataFrame

    def to_coco(self) -> dict:
        coco = dataframe_to_coco(annotations_df)
        coco['images'] =

    @staticmethod
    def dataframe_to_coco(dataset: pd.core.frame.DataFrame):
        """
        Most frameworks train from COCO annotation files.

        Dataframes are much easier to work with and manipulate
        The COCO bounding box format is [top left x position, top left y position, width, height].
        """
        print(dataset.columns.tolist())

        data = {}

        data['info'] = {
         'year': '',
         'version': '',
         'description': '',
         'contributor': '',
         'url': '',
         'date_created': ''
        }

        data['licences'] = [{'name': '', 'id': 0, 'url': ''}]

        columns = ['name','category_id']
        data['categories'] = dataset[columns]\
                    .rename(columns={'category_id': 'id'})\
                    .drop_duplicates()\
                    .to_dict(orient='records')

        columns = ['image_id','file_name', 'height', 'width']
        data['images'] = dataset[columns]\
                    .rename(columns={'image_id': 'id'})\
                    .drop_duplicates()\
                    .to_dict(orient='records')

        columns = ['annotation_id','image_id', 'category_id', 'bbox', 'area', 'iscrowd', 'supercategory', 'rotation', 'occluded', 'label_id']
        dataset['bbox'] = dataset['bbox'].astype(str)

        intermediate = dataset[columns]\
                                .rename(columns={'annotation_id': 'id'})\
                                .drop_duplicates()\

        intermediate['bbox'] = intermediate['bbox'].apply(ast.literal_eval)

        data['annotations'] = intermediate.to_dict(orient='records')

        print('Completed conversion to COCO dict structure')
        return data


    def from_coco(data: dict) -> pd.core.frame.DataFrame:
        categories_df = pd.json_normalize(data['categories'])
        annotations_df = pd.json_normalize(data['annotations'])
        annotations_df['annotation_id'] = annotations_df['id']
        images_df = pd.json_normalize(data['images'])
        images_annotations_df = pd.merge(images_df, annotations_df, left_on='id', right_on='image_id')
        files_without_annotations = ...
        return CocoFrame (
            annotations_df = pd.merge(images_annotations_df, categories_df, left_on='category_id', right_on='id'),
            empty_frames =
        )
