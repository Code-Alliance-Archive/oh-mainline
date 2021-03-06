
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Company', 0, 'text', 1, 'Company, Organization, or Event Where You Learned About SocialCoding4Good');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Organizations', 0, 'multi', 2, 'HFOSS Organizations That Interest You');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Causes', 0, 'multi', 3, 'Causes That Interest You');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Time to Commit', 1, 'multi', 4, 'How much time would you like to commit to volunteering?');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Skills', 1, 'multi', 5, 'Skills');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Resume', 0, 'file', 6, 'Resume');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('LinkedIn, OpenHatch or CoderWall Profile URL', 0, 'url', 7, 'LinkedIn, OpenHatch or CoderWall Profile URL');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Have you previously contributed to open source projects?', 0, 'single', 8, 'Have you previously contributed to open source projects?');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('GitHub Username', 0, 'text', 9, 'GitHub Username');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Google Code Username', 0, 'text', 10, 'Google Code Username');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('SourceForge, Ohloh or Other Username', 0, 'text', 11, 'SourceForge, Ohloh or Other Username');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Languages', 0, 'multi', 12, 'Programming Languages, Frameworks, Environments');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Experience Level', 0, 'single', 13, 'Experience Level');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('What languages do you speak, read, and write?', 0, 'text', 14, 'What languages do you speak, read, and write?');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('How did you hear about SocialCoding4Good?', 0, 'multi', 15, 'How did you hear about SocialCoding4Good?');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Would you like us to keep you posted on the latest news from SocialCoding4Good?', 0, 'single', 16, 'Would you like us to keep you posted on the latest news from SocialCoding4Good?');
INSERT OR IGNORE INTO profile_formquestion (name, required, type, id, display_name) VALUES ('Comments or Questions', 0, 'textarea', 17, 'Comments or Questions');

INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Benetech');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Code for America');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'FrontlineSMS');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'The Guardian Project');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Medic Mobile');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Mifos');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Sahana Software');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'SocialCoding4Good');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Amara (Universal Subtitles)');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Ushahidi');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (2, 'Wikimedia Foundation');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Civic Engagement');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Climate Change Mitigation');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Disaster Relief');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Education and Literacy');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Empowerment of Women');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Environmental and Species Conservation');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Healthcare');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Homelessness');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Human Rights');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Poverty Alleviation');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (3, 'Self Sufficiency for People with Disabilities');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (4, 'A Few Hours per Week');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (4, 'A Few Hours per Month');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (4, '0-8 Hours Total');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (4, '8-20 Hours Total');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (4, '20-40 Hours Total');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (4, 'More Than 40 Hours Total');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (4, 'Unknown');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Software Development');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'User Interface Design');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Product Management');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Community Management');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Quality Assurance');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Project Management / Scrummaster');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Systems Administration');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Technical Documentation');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (5, 'Technical Support');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (8, 'Yes');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (8, 'No');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'ActionScript');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'C');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'C++');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'C#');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Django');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'HTML/CSS');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Java');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Java on Android');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'JavaScript');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Lua');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Objective C');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Objective C on iPhone');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Perl');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'PHP');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Python');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Ruby');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Scala');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Swing');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (12, 'Other');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (13, 'Beginner');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (13, 'Intermediate');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (13, 'Expert');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (15, 'Media or News Coverage');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (15, 'Word of Mouth');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (15, 'Conference or Event');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (15, 'Company Where You Work');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (15, 'Social Media');
INSERT OR IGNORE INTO profile_formanswer (question_id, value) VALUES (16, 'Yes please!');

INSERT OR IGNORE INTO profile_carddisplayedquestion (id, person_id, question_id) VALUES (1, 1, 1);
INSERT OR IGNORE INTO profile_carddisplayedquestion (id, person_id, question_id) VALUES (2, 1, 2);
INSERT OR IGNORE INTO profile_carddisplayedquestion (id, person_id, question_id) VALUES (3, 1, 3);
INSERT OR IGNORE INTO profile_carddisplayedquestion (id, person_id, question_id) VALUES (4, 1, 4);
INSERT OR IGNORE INTO profile_carddisplayedquestion (id, person_id, question_id) VALUES (5, 1, 5);
INSERT OR IGNORE INTO profile_carddisplayedquestion (id, person_id, question_id) VALUES (6, 1, 12);
