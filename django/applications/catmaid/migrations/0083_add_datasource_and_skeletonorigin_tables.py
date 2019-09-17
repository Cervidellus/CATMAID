from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


forward = """
    CREATE TABLE data_source (
        id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        user_id int REFERENCES auth_user(id) NOT NULL,
        project_id int REFERENCES project(id) ON DELETE CASCADE NOT NULL,
        creation_time timestamptz NOT NULL DEFAULT now(),
        edition_time timestamptz NOT NULL DEFAULT now(),
        name text DEFAULT NULL,
        url text NOT NULL,
        txid bigint DEFAULT txid_current(),

        UNIQUE(project_id, url),
        UNIQUE(project_id, name)
    );

    CREATE TYPE skeleton_origin_source_type AS ENUM ('skeleton', 'segmentation');

    CREATE TABLE skeleton_origin (
        id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        user_id int REFERENCES auth_user (id) NOT NULL,
        project_id int REFERENCES project(id) ON DELETE CASCADE NOT NULL,
        creation_time timestamptz NOT NULL DEFAULT now(),
        edition_time timestamptz NOT NULL DEFAULT now(),
        skeleton_id bigint REFERENCES class_instance(id) ON DELETE CASCADE NOT NULL,
        data_source_id integer REFERENCES data_source(id) ON DELETE CASCADE NOT NULL,
        source_id bigint NOT NULL,
        txid bigint DEFAULT txid_current(),
        source_type skeleton_origin_source_type
    );

    -- Setup history
    SELECT create_history_table('data_source'::regclass, 'edition_time', 'txid');
    SELECT create_history_table('skeleton_origin'::regclass, 'edition_time', 'txid');

    -- Create indices
    CREATE INDEX skeleton_origin_skeleton_id_idx ON skeleton_origin (skeleton_id);
    CREATE INDEX skeleton_origin_data_source_id_idx ON skeleton_origin (data_source_id);
    CREATE INDEX skeleton_origin_source_id_idx ON skeleton_origin (source_id);

    CREATE INDEX skeleton_origin__history_skeleton_id_idx
        ON skeleton_origin__history (skeleton_id);
    CREATE INDEX skeleton_origin__history_data_source_id_idx
        ON skeleton_origin__history (data_source_id);
    CREATE INDEX skeleton_origin__history_source_id_idx
        ON skeleton_origin__history (source_id);
"""

backward = """
    SELECT drop_history_table('skeleton_origin'::regclass);
    SELECT drop_history_table('data_source'::regclass);

    DROP TABLE skeleton_origin;
    DROP TABLE data_source;

    DROP TYPE skeleton_origin_source_type;
"""

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catmaid', '0082_add_parent_node_to_treenode_edge'),
    ]

    operations = [
        migrations.RunSQL(forward, backward, [
            migrations.CreateModel(
                name='DataSource',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('edition_time', models.DateTimeField(default=django.utils.timezone.now)),
                    ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                    ('name', models.TextField(blank=True, default=None, null=True)),
                    ('url', models.TextField()),
                    ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catmaid.Project')),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ],
                options={
                    'db_table': 'data_source',
                },
            ),
            migrations.CreateModel(
                name='SkeletonOrigin',
                fields=[
                    ('edition_time', models.DateTimeField(default=django.utils.timezone.now)),
                    ('skeleton', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='catmaid.ClassInstance')),
                    ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                    ('source_id', models.IntegerField()),
                    ('source_type', models.TextField()),
                    ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catmaid.DataSource')),
                    ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catmaid.Project')),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ],
                options={
                    'db_table': 'skeleton_origin',
                },
            ),
        ]),
    ]