from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


forward = """
    CREATE TYPE volume_origin_source_type AS ENUM ('mesh', 'segmentation');

    CREATE TABLE volume_origin (
        id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        user_id int REFERENCES auth_user (id) NOT NULL,
        project_id int REFERENCES project(id) ON DELETE CASCADE NOT NULL,
        creation_time timestamptz NOT NULL DEFAULT now(),
        edition_time timestamptz NOT NULL DEFAULT now(),
        volume_id bigint REFERENCES class_instance(id) ON DELETE CASCADE NOT NULL,
        data_source_id integer REFERENCES data_source(id) ON DELETE CASCADE NOT NULL,
        source_id bigint NOT NULL,
        txid bigint DEFAULT txid_current(),
        source_type volume_origin_source_type
    );

    -- Setup history
    SELECT create_history_table('volume_origin'::regclass, 'edition_time', 'txid');

    -- Create indices
    CREATE INDEX volume_origin_volume_id_idx ON volume_origin (volume_id);
    CREATE INDEX volume_origin_data_source_id_idx ON volume_origin (data_source_id);
    CREATE INDEX volume_origin_source_id_idx ON volume_origin (source_id);

    CREATE INDEX volume_origin__history_volume_id_idx
        ON volume_origin__history (volume_id);
    CREATE INDEX volume_origin__history_data_source_id_idx
        ON volume_origin__history (data_source_id);
    CREATE INDEX volume_origin__history_source_id_idx
        ON volume_origin__history (source_id);
"""

backward = """
    SELECT drop_history_table('volume_origin'::regclass);

    DROP TABLE volume_origin;

    DROP TYPE volume_origin_source_type;
"""

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catmaid', '0112_add_spaces_data_view'),
    ]

    operations = [
        migrations.RunSQL(forward, backward, [
            migrations.CreateModel(
                name='SkeletonOrigin',
                fields=[
                    ('edition_time', models.DateTimeField(default=django.utils.timezone.now)),
                    ('volume', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='catmaid.ClassInstance')),
                    ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                    ('source_id', models.IntegerField()),
                    ('source_type', models.TextField()),
                    ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catmaid.DataSource')),
                    ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catmaid.Project')),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ],
                options={
                    'db_table': 'volume_origin',
                },
            ),
        ]),
    ]
