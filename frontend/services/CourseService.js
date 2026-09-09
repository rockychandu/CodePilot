/* Course & Learning Service */
import { mockCourses } from '../mock-data/courses.js';
import { sleep } from '../utils/helpers.js';

export class CourseService {
  static async getCourses(category = 'All') {
    await sleep(200);
    if (!category || category === 'All') return mockCourses;
    return mockCourses.filter(c => c.category.toLowerCase() === category.toLowerCase());
  }

  static async getCourseById(id) {
    await sleep(150);
    const course = mockCourses.find(c => c.id === id);
    if (!course) throw new Error('Course not found');
    return course;
  }
}
