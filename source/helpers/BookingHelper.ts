import moment from "moment";
import { Form, Question, Step } from "../types/FormTypes";
import { TimeSlot } from "../components/molecules/TimeSlotPicker/TimeSlotPicker";

type TimeSpan = {
  startTime: string;
  endTime: string;
};

export type Administrator = {
  title: string;
  department: string;
  jobTitle: string;
  email: string;
  phone: string;
};

export type BookingItem = {
  date: string;
  time: { startTime: string; endTime: string };
  title: string;
  status: string;
  administrator: Administrator;
  addressLines: string[];
};

type GraphData = {
  BookingId: string;
  Subject: string;
  Body: string;
  Location: string;
  ReferenceCode: string;
  StartTime: string;
  EndTime: string;
  Attendees: {
    Email: string;
    Type: string;
    Status: string;
  }[];
};

export type TimeSlotDataType = Record<string, Record<string, TimeSpan[]>>;

const mockAdministrator: Administrator = {
  title: "Lex Luthor",
  department: "Socialförvaltningen",
  jobTitle: "Socialsekreterare",
  email: "kontaktcenter@helsingborg.se",
  phone: "042 - 00 00 00",
};

function formDataToQuestions(formData: Form): Question[] {
  return formData.steps
    .flatMap((step: Step) => step.questions)
    .filter(
      (question: Question | undefined): question is Question =>
        question !== undefined
    );
}

function timeSpanToString(timeSpan: TimeSpan | TimeSlot): string {
  return `${timeSpan.startTime}-${timeSpan.endTime}`;
}

function compareTimeSlots(a: TimeSlot, b: TimeSlot) {
  return timeSpanToString(a).localeCompare(timeSpanToString(b));
}

/**
 * @description Takes a timeSlots object output by the backend and propagates information from
 * the higher levels to the innermost objects, while also joining the timetables of all admins
 */
function consolidateTimeSlots(
  timeSlots: TimeSlotDataType
): Record<string, TimeSlot[]> {
  /**
   * First we do the joining, by using the timespan as a property.
   * This allows the data to be used for booking a service.
   * We will go from format:
   * {email: {date: [{ startTime, endTime }]}}
   * To format:
   * {date: {time: { startTime, endTime, date, emails }}}
   */
  const joinedTimeSlots: Record<string, Record<string, TimeSlot>> = {};
  const emails = Object.keys(timeSlots);
  emails.forEach((email) => {
    const dates = Object.keys(timeSlots[email]);
    dates.forEach((date) => {
      timeSlots[email][date].forEach((timeSpan: TimeSpan) => {
        const timeString = timeSpanToString(timeSpan);
        if (joinedTimeSlots[date] === undefined) {
          joinedTimeSlots[date] = {};
        }
        if (joinedTimeSlots[date][timeString] === undefined) {
          const newObject: TimeSlot = { ...timeSpan, date, emails: [email] };
          joinedTimeSlots[date][timeString] = newObject;
        } else {
          const oldEmails: string[] = joinedTimeSlots[date][timeString].emails;
          joinedTimeSlots[date][timeString].emails = [...oldEmails, email];
        }
      });
    });
  });
  /**
   * We have done one pass over the data, newTimeSlots is now in format:
   * {date: {time: { startTime, endTime, date, emails }}}
   * We want the data to be in the format:
   * {date: [{ startTime, endTime, date, emails }]}
   */
  const reformattedTimeSlots: Record<string, TimeSlot[]> = {};
  const dates = Object.keys(joinedTimeSlots);
  dates.forEach((date) => {
    const timeList = Object.values(joinedTimeSlots[date]);
    timeList.sort(compareTimeSlots);
    reformattedTimeSlots[date] = timeList;
  });
  return reformattedTimeSlots;
}

const convertGraphDataToBookingItem = (graphData: GraphData): BookingItem => {
  const firstAttendee = graphData.Attendees[0];
  const administrator = { ...mockAdministrator, email: firstAttendee.Email };
  const status = firstAttendee.Status;
  const date = moment(graphData.StartTime).format("YYYY-MM-DD");
  const startTime = moment(graphData.StartTime).format("HH:mm:ss");
  const endTime = moment(graphData.EndTime).format("HH:mm:ss");
  const title = graphData.Subject.substring(0, graphData.Subject.indexOf("#"));
  return {
    date,
    time: { startTime, endTime },
    title,
    status,
    administrator,
    addressLines: [graphData.Location],
  };
};

export {
  formDataToQuestions,
  consolidateTimeSlots,
  convertGraphDataToBookingItem,
  mockAdministrator,
};