from sqlalchemy import Integer, and_, cast, func, select, insert
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager

from models import ResumesOrm, WorkersOrm


class SyncORM:
    @staticmethod
    def create_tables(Base, engine_sync):
        # engine_sync.echo = False
        Base.metadata.drop_all(engine_sync)
        Base.metadata.create_all(engine_sync)

    # insert (добавление) через орм.
    @staticmethod
    def insert_workers(
        session_factory,
        WorkersOrm,
        first_username: str,
        second_username: str,
    ):
        with session_factory() as session:

            # Вариант для добавления всех нужных элементов:
            worker_bobr = WorkersOrm(username=first_username)
            worker_volk = WorkersOrm(username=second_username)
            session.add_all([worker_bobr, worker_volk])

            # Вариант для добавления одного элемента:
            # stmt = insert(table=WorkersOrm).values(username="Dima")
            # session.execute(stmt)
            session.flush()  # отправляем измененеия в базу и еще не завершаем запрос
            session.commit()  # отправляем изменения в базу и завершает запрос

    # SELECT
    @staticmethod
    def select_workers(
        sync_session_factory,
        WorkersOrm,
        id: int = 1,
    ):
        with sync_session_factory() as session:
            # worker = session.get(WorkersOrm, id) - получаем одного работника
            query = select(WorkersOrm)  # SELECT * FROM WorkersOrm
            result = session.execute(query)
            # workers = (
            #     result.all()
            # )  # sqlalchemy возвращает список из кортежей моделей воркеров (создает экземпляры наших моделей)

            workers = (
                result.scalars().all()
            )  # scalars возвращает первое значение каждого кортежа
            print([el.username for el in workers])

    # UPDATE
    @staticmethod
    def update_worker(
        sync_session_factory,
        WorkersOrm,
        new_username: str,
        worker_id: int = 2,
    ):
        with sync_session_factory() as session:
            # СЫРОЙ UPDATE запрос:
            # stmt = text(
            #     "UPDATE workers SET username=:username WHERE id=:worker_id"
            # )  # сырой запрос
            # stmt = stmt.bindparams(username=new_username, worker_id=worker_id)
            # session.execute(stmt)
            # session.commit()

            # запрос в стиле orm но мы делаем 2 запроса к бд (1й - запрашиваем воркера, 2й- изменяем его)
            worker = session.get(
                WorkersOrm, worker_id
            )  # - получаем нужного работника из бд
            worker.username = (
                new_username  # просто изменяем (мутируем) экземпляр класса
            )
            # session.expire_all()  # сбрасывает изменения
            session.refresh(worker)
            # Принцип работы refresh: когда код доходит ДО рефреш - Python изменяет данные на те которые мы указали при изменении но они еще не отправили в бд. REFRESH запрашивает данные которые были ДО изменения и обновляет у нас локально их до исходных. Забирает последнее обновление с бд.
            session.commit()

    @staticmethod
    def insert_resumes(
        sync_session_factory,
        model,
        # **kwargs
        compensation,
        title,
        workload,
        worker_id,
    ):
        with sync_session_factory() as session:
            resume = model(
                compensation=compensation,
                workload=workload,
                title=title,
                worker_id=worker_id,
            )
            session.add(resume)
            session.commit()

    #  считаем авг зарплату по каждому типу нагруженности (workload)
    @staticmethod
    def select_resumes_avg_compensation(
        sync_session_factory, table, language: str = "Python"
    ):
        with sync_session_factory() as session:
            # Выбери строки workload из таблицы resumes где указан в тайтле "Python" и зарплата выше 40000
            # в итоге получим 2 ответа: авг по запрлате с нагруженностью fulltime и parttime с "python" в тайтле
            """SELECT workload, avg(compensation)::int as avg_compensation
            from resumes
            WHERE title like '%Python%' and compensation > 40000
            group by workload
            """

            query = (
                select(
                    table.workload,
                    cast(func.avg(table.compensation), Integer).label(
                        "avg_compensation"
                    ),
                )
                .select_from(table)
                .filter(
                    and_(table.title.contains(language)), table.compensation > 40000
                )
                .group_by(table.workload)
            )
            # print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)

    # Проблема N + 1 - это когда мы подгружаем какие то сущности а потом чтобы посмотреть связаные с ними другие данные с другой таблицы делаем еще один запрос для подсущности этой сущности, чтобы например запросить резюме конкретного воркера.
    # @staticmethod
    # def select_workers_with_lazy_relationship(session, worker_model):
    #     with session() as session:
    #         query = select(worker_model)
    #         res = session.execute(query)
    #         result = res.scalars().all()
    #         worker_1_resume = result[0].resumes
    #         print(worker_1_resume)

    #         worker_2_resume = result[1].resumes
    #         print(worker_2_resume)

    # joinload - подходит только для one2one или many2one. При использовании many2one - он будет подгружать много лишних данных которые будут дублироваться в таблице
    # с помощью relationship можно отправить один большой запрос с нашими нужными сущностями и прикрепленными к ним подсущности с другой таблицы (resume)
    @staticmethod
    def select_workers_with_join_relationship(session, worker_model):
        with session() as session:
            query = select(worker_model).options(joinedload(worker_model.resumes))
            res = session.execute(query)
            result = (
                res.unique().scalars().all()
            )  # unique - чтобы не повторялись сущности с один айди
            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)

    # selectinload - используется для связки one2many или many2many
    # при этом виде подгрузки мы подгружаем сначало всех воркеров а потом все резюме тех воркеров которые мы подгрузили
    @staticmethod
    def select_in_workers_with_join_relationship(session, worker_model):
        with session() as session:
            query = select(worker_model).options(selectinload(worker_model.resumes))
            res = session.execute(query)
            result = (
                res.unique().scalars().all()
            )  # unique - чтобы не повторялись сущности с один айди
            worker_1_resume = result[0].resumes
            print(worker_1_resume)

            worker_2_resume = result[1].resumes
            print(worker_2_resume)

    # Запрос через отдельный relationship с нужными фильтрами
    @staticmethod
    def select_workers_with_cond_relationship(session, worker_table):
        with session() as session:
            query = select(worker_table).options(
                selectinload(worker_table.resumes_parttime)
            )
            res = session.execute(query)
            result = res.scalars().all()
            print(result)

    # contains_eager
    @staticmethod
    def select_workers_with_cond_relationship_contains_eager(
        session, worker_table, resume_table
    ):
        with session() as session:
            query = (
                select(worker_table)
                .join(worker_table.resumes)
                .options(contains_eager(worker_table.resumes))
                .filter(resume_table.workload == "parttime")
            )
            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)

    @staticmethod
    def select_workers_with_cond_relationship_contains_eager_with_limit(
        session, worker_table, resume_table
    ):
        with session() as session:
            subq = (
                select(resume_table.id.label("parttime_resume_id"))
                .filter(resume_table.worker_id == worker_table.id)
                .order_by(worker_table.id.desc())
                .limit(2)  # Мы хотим только одно резюме у каждого работника
                .scalar_subquery()
                .correlate(worker_table)
            )

            query = (
                select(worker_table)
                .join(resume_table, resume_table.id.in_(subq))
                .options(contains_eager(worker_table.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()
            print(result)


class AsyncORM:
    @staticmethod
    async def async_insert_data(WorkersOrm, async_session_factory):
        async with async_session_factory() as session:
            worker = WorkersOrm(username="New Worker from orm")
            session.add(worker)
            # resume = ResumesOrm(
            #     title="New resume",
            #     compensation=23,
            #     workload="parttime",
            #     worker_id=2,
            # )
            # session.add(resume)
            await session.commit()

    @staticmethod
    # Get запрос через орм
    async def get_worker_by_id(async_session_factory, WorkersOrm, id: int):
        async with async_session_factory() as session:
            result = await session.get(WorkersOrm, id)
            print(result.username)
        # query = select(WorkersOrm).where(WorkersOrm.id == id)
        # result = await session.execute(query)
        # print(result.scalar())

    @staticmethod
    async def insert_additional_resumes(
        sync_session_factory,
        table_workers,
        table_resumes,
        resumes,
        workers,
    ):
        async with sync_session_factory() as session:
            query_workers = insert(table_workers).values(workers)
            query_resumes = insert(table_resumes).values(resumes)
            await session.execute(query_workers)
            await session.execute(query_resumes)
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func(
        session,
        like_language: str = "Python",
    ):
        # Задача: составить одну таблицу из двух где будут имена воркеров, их резюме с зарплатами и должна быть колонка насколько отклонена зарплата воркера от средней зарплаты по рынку
        """
        WITH helper2 AS (
            SELECT *, compensation - avg_workload_compensation AS compensation_diff
            FROM
                (SELECT
                    w.id,
                    w.username,
                    r.compensation,
                    r.workload,
                    avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
                FROM resumes r
                JOIN workers w ON r.worker_id = w.id) helper1
            )
            SELECT * FROM helper2
            ORDER BY compensation_diff DESC
        """
        async with session() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation)
                    .over(partition_by=r.workload)
                    .cast(Integer)
                    .label("avg_workload_compensation"),
                )
                .select_from(r)
                .join(w, r.worker_id == w.id)
                .subquery("helper1")
            )
            cte = select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label(
                    "compensation_diff"
                ),
            ).cte("helper2")
            query = select(cte).order_by(cte.c.compensation_diff.desc())

            res = await session.execute(query)
            result = res.all()
            for el in result:
                print(el)

            # print(query.compile(compile_kwargs={"literal_binds": True}))
