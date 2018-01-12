CREATE TABLE `bill_book`
(
  id               INT AUTO_INCREMENT
    PRIMARY KEY,
  bill_keeper      VARCHAR(255)       NOT NULL
  COMMENT '账单记录人',
  bill_amount      DOUBLE DEFAULT '0' NULL
  COMMENT '账单金额',
  bill_description VARCHAR(255)       NULL
  COMMENT '账单描述',
  is_valid         INT                NOT NULL
  COMMENT '0：记录无效，1：记录有效',
  created_time     DATETIME           NOT NULL,
  updated_time     DATETIME           NOT NULL,
  CONSTRAINT bill_book_id_uindex
  UNIQUE (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;