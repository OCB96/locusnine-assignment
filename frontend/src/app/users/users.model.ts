export class User {
  constructor(
    public name: string,
    public email: string,
    public role_type: string,
    public mobile_number: string,
    public activity_status: string,
    public _id?: number,
    public updatedAt?: Date,
    public createdAt?: Date,
    public lastUpdatedBy?: string,
  ) { }
}
