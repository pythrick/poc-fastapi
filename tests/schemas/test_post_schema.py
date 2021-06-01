from poc_fastapi.schemas.post import PostSchema


def test_post_schema(post):
    post_schema = PostSchema.from_orm(post)
    assert isinstance(post_schema, PostSchema)
