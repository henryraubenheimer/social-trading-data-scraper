import peewee

db = peewee.MySQLDatabase(
    'etoro',
    user='henry',
    password='henry12345',
    host='scrape.mercusysddns.com',
    port=3306
)

class investor(peewee.Model):

    name = peewee.TextField(primary_key=True)
    profit = peewee.FloatField()
    risk = peewee.IntegerField()
    copiers = peewee.IntegerField()

    class Meta:

        database = db
        table_name = 'investor'


class share(peewee.Model):

    ticker = peewee.TextField(primary_key=True)

    class Meta:

        database = db
        table_name = 'share'


class share_position(peewee.Model):

    investor = peewee.ForeignKeyField(investor, column_name='investor', backref='positions', on_delete='CASCADE', on_update='CASCADE')
    share = peewee.ForeignKeyField(share, column_name='share', backref='positions', on_delete='CASCADE', on_update='CASCADE')
    direction = peewee.TextField()
    invested = peewee.FloatField()
    profit_loss = peewee.FloatField()
    value = peewee.FloatField()

    class Meta:

        database = db
        table_name = 'share_position'
        primary_key = peewee.CompositeKey('investor', 'share')


class transaction(peewee.Model):

    id = peewee.UUIDField(primary_key=True)
    time = peewee.DateTimeField()
    investor = peewee.ForeignKeyField(investor, column_name='investor', backref='transactions', on_delete='CASCADE', on_update='CASCADE')
    share = peewee.ForeignKeyField(share, column_name='share', backref='transactions', on_delete='CASCADE', on_update='CASCADE')
    buy = peewee.BooleanField()
    amount = peewee.FloatField()
    leverage = peewee.FloatField()
    open = peewee.FloatField()
    profit_loss = peewee.IntegerField()
    sl = peewee.FloatField()

    class Meta:

        database = db
        table_name = 'transaction'