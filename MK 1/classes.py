import peewee

db = peewee.MySQLDatabase(
    'etoro',
    user='henry',
    password='henry12345',
    host='scrape.mercusysddns.com',
    port=3306
)

class investor(peewee.Model):

    id = peewee.UUIDField(primary_key=True)
    name = peewee.TextField()
    strategy = peewee.TextField()
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

    id = peewee.UUIDField(primary_key=True)
    investor_id = peewee.ForeignKeyField(investor, backref='positions')
    share = peewee.ForeignKeyField(share, column_name='share', backref='positions')
    direction = peewee.TextField()
    invested = peewee.FloatField()
    profit_loss = peewee.FloatField()
    value = peewee.FloatField()

    class Meta:

        database = db
        table_name = 'share_position'


class transaction(peewee.Model):

    id = peewee.UUIDField(primary_key=True)
    time = peewee.DateTimeField()
    investor_id = peewee.ForeignKeyField(investor, backref='transactions')
    share = peewee.ForeignKeyField(share, column_name='share', backref='transactions')
    buy = peewee.BooleanField()
    amount = peewee.FloatField()
    leverage = peewee.IntegerField()
    open = peewee.FloatField()
    profit_loss = peewee.FloatField()
    sl = peewee.FloatField()

    class Meta:

        database = db
        table_name = 'transaction'