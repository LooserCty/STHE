DROP TABLE IF EXISTS project_t;
DROP TABLE IF EXISTS time_t;
-- DROP TABLE IF EXISTS geology_t;
-- DROP TABLE IF EXISTS segment_t;
-- DROP TABLE IF EXISTS disease_t;
-- DROP TABLE IF EXISTS solution_t；



CREATE TABLE project_t(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text UNIQUE not NULL,
    describe text not null,
    depth real not NULL,
    radiusInside real not null,
    radiusOuter real not null,
    length real not null,
    strength real not null,

    user_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_t(id)
);

CREATE TABLE time_t(
    id integer PRIMARY KEY AUTOINCREMENT,
    date text not null,

    project_id integer not null,
    FOREIGN KEY (project_id) REFERENCES project_t(id)
);


-- CREATE TABLE geology_t(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     depth real not NULL,
--     radius_inside real not null,
--     radius_outer real not null,
--     concrete text not null,
--     strength real not null,

--     project_id integer NOT NULL,
--     FOREIGN KEY (project_id) REFERENCES project_t(id)
-- );

-- CREATE TABLE segment_t(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     number integer unique not null,

--     project_id integer NOT NULL,
--     FOREIGN KEY (project_id) REFERENCES project_t(id)
-- );

-- CREATE TABLE disease_t(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     acquisitionTime text not null,
--     crackLength real not null,
--     crackWidth real not null,
--     radiusOfCurvature real not null,
--     segmentDislocation real not null,
--     settlementRate real not null,
--     convergenceDeformation real not null,
--     leakageRate text not null,

--     segment_id integer NOT NULL,
--     FOREIGN KEY (segment_id) REFERENCES segment_t(id)
-- );

-- CREATE TABLE solution_t(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,

--     acquisitionTime text not null,

--     crackLength integer not null,
--     crackWidth integer not null,
--     radiusOfCurvature integer not null,
--     segmentDislocation integer not null,
--     settlementRate integer not null,
--     convergenceDeformation integer not null,
--     leakageRate integer not null,

--     subjection1 real not null,
--     subjection2 real not null,
--     subjection3 real not null,
--     subjection4 real not null,

--     comprehensiveValue real not null,
--     comprehensiveLevel integer not null,

--     segment_id integer NOT NULL,
--     FOREIGN KEY (segment_id) REFERENCES segment_t(id)
-- );
