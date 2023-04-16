SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for key_repo
-- ----------------------------
DROP TABLE IF EXISTS `key_repo`;
CREATE TABLE `key_repo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for project_source
-- ----------------------------
DROP TABLE IF EXISTS `project_source`;
CREATE TABLE `project_source` (
  `id` int(11) NOT NULL,
  `project_name` varchar(255) NOT NULL,
  `repo_link` varchar(255) NOT NULL,
  `language` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `foundation` varchar(255) DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  `last_scan` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repo_link` (`repo_link`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for scan_result
-- ----------------------------
DROP TABLE IF EXISTS `scan_result`;
CREATE TABLE `scan_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `report` text,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `project_id` FOREIGN KEY (`project_id`) REFERENCES `project_source` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113059 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
INSERT INTO  `user` VALUES (1,"admin","aDmin13344");
SET FOREIGN_KEY_CHECKS = 1;
