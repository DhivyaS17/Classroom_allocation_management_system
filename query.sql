-- Active: 1690477172856@@127.0.0.1@3306@user_db
create table users(uname VARCHAR(100),upassword VARCHAR(100));

drop table users;

CREATE table session_allocation(StaffName VARCHAR(50),Description VARCHAR(50),sessionDate VARCHAR(10),fperiod VARCHAR(10),tperiod VARCHAR(10),PhoneNUmber VARCHAR(10),SessionID VARCHAR(10));

CREATE PROCEDURE session_checker(
  IN sname VARCHAR(50),
  IN sdate VARCHAR(10),
  IN time1 VARCHAR(10),
  IN time2 VARCHAR(10),
  OUT result INT)

BEGIN
  -- Check if the session already exists
  SELECT COUNT(*)
  INTO result
  FROM session_allocation
  WHERE sessionDate = sdate
  AND fperiod = time1
  AND tperiod = time2;

  -- If the session already exists, check if the staff member is already allocated to the session
  IF result > 0 THEN
    SELECT COUNT(*)
    INTO result
    FROM session_allocation
    WHERE sessionDate = sdate
    AND fperiod = time1
    AND tperiod = time2
    AND staffName = sname;

    -- If the staff member is already allocated to the session, set the result to 2
    IF result > 0 THEN
      SET result := 2;
    END IF;
  END IF;
END;


CREATE Trigger after_in BEFORE INSERT
on session_allocation
for each row
BEGIN
declare nid varchar(10);
SET nid=CONCAT(SUBSTRING(NEW.sessionDate,9),'_',NEW.fperiod,NEW.tperiod);
SET NEw.SessionId=nid;
END;
